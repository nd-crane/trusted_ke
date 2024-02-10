import functools
import multiprocessing
import time

import tensorflow as tf

import nltk
nltk.download('stopwords')

import numpy as np

from transformers import T5Tokenizer
tokenizer_mt5 =  T5Tokenizer.from_pretrained('google/mt5-xxl')

# NEEDS IMPLEMENTATION depending on the infrastructure
def predictor_fn(docs):
  """The method takes a batch of documnets and processes each.

  Args:
    docs: list[str] list of document strings (obtained by the state.get_input_annotation method).

  Returns:
    predictions: list[str] (output text predicted by the mt5 model).
  """

  predictions = []

  for i_doc, doc in enumerate(batches):

    ## how to actually implement?
    result = f"Doc {i_doc}: {doc}"

    predictions.append(result)

  return predictions

def predict_coreferences(batches, threads_to_use=1):
  """Predict coreferences of focus part (e.g. one sentence)"""

  with multiprocessing.pool.ThreadPool(threads_to_use) as pool:
    results = pool.map(predictor_fn, batches)

  return results

def extract_result_string(predictions):
  """Extract the results from prediction."""

  results = []
  for batch in predictions:
    #output_text = tf.make_ndarray(resp)

    for text in batch:
      #text = text[0].decode('utf-8')
      results.append(text)

  return results

########## Extract Coreferences

# @title helper
def normalize_speaker(speaker_in):
  """Add '_' before and after speaker name if it does not contain it already"""
  if speaker_in == '-' or speaker_in == '__':
    return '_'

  speaker = speaker_in.replace(' ', '_')
  speaker = speaker.strip()

  if not speaker.startswith('_'):
    speaker = '_'+speaker
  if not speaker.endswith('_'):
    speaker = speaker+'_'
  return speaker


def match_mention_state(m, inputs, maps, position=None, debug=False, start_index=0):

  if '##' in m:
    index_num = m.index('##')
  else:
    if not m[0].startswith('['):
      print('get_chains::error ## not in split', m)
    index_num = len(m)

  if ']]' in inputs:
    end_index = inputs.index(']]')
  elif '**' in inputs:
    end_index = inputs.index('**')
  else:
    end_index = len(inputs)

  # m_clean = [x for x in m if x != '##']
  m_clean = []
  for x in m:
    if x != '##':
      m_clean.append(x)
    if x == '**':
      break

  # get context
  context = []
  found_num = False
  for s in m:
    if found_num:
      context.append(s)
    if '##' == s:
      found_num = True

  maps_index = 0
  indices = []
  for i in range(start_index, end_index):
    maps_index = i
    if inputs[i] == m_clean[0]:
      if inputs[i:i+len(m_clean)] == m_clean:
        indices.append((maps[maps_index], maps[maps_index + index_num  - 1]))

        if maps[maps_index + index_num  - 1] == -1:
          print('index negative', maps[maps_index:], ' index_num',  index_num)
          print('index negative', inputs[i:], ' index_num',  index_num)
          print(f'i {i} maps_index {maps_index}')


  if len(indices) == 0:
    print('none found match_mention', m)
    print('inputs', inputs)
    return []
  elif len(indices) > 1 and debug:
    print('match_mention: too many ', m,  indices, 'm_clean - use both')

  if (-1,-1) in indices:
    print('error for ',m, indices)
    return []

  return indices

def match_link_state(link, inputs, maps, cluster_name_to_cluster,
                     debug=True, node_wise=True):
  link_mentions = [m.split(' ') for m in link]
  links = []
  if len(link_mentions) == 1 and node_wise:
    m0 = link_mentions[0]
    try:
      index_m0 = match_mention_state(m0, inputs, maps, position=None)
      links = [index_m0]
    except Exception as e:
      print(str(e))
    return links


  m0 = link_mentions[0]
  m1 = link_mentions[1]

  if debug:
    print('match_link', m0, m1)

  # invert indices
  if m1[0].startswith('[') and len(m1[0]) > 0:
    cluster = cluster_name_to_cluster.get(m1[0], None)
    if cluster is not None:
      index_m1 = [cluster[-1]]
    else:
      print('cluster does not exists')
      return []
  else:
    index_m1 = match_mention_state(m1, inputs, maps, position=None)


  if debug:
    print(index_m1 ,'match' ,m1)

  if len(index_m1) > 1:
    print('index_m1', index_m1)

  try:
    index_m0 = match_mention_state(m0, inputs, maps, position=None)
  except Exception as e:
    print('error', str(e))
    index_m0 = []

  if debug:
    print(index_m0 ,'match' , m0)

  if len(index_m0) > 1:
    print('index_m0', index_m0)

  if len(index_m1) > 0 and len(index_m0) > 0:
      i1 = index_m1[-1]
      i2 = index_m0[-1]
      links.append([i1, i2])

  # use only last link
  if len(links) > 1:
    print('too many links, ', links, 'for link', link)
    print('context', inputs)

    return links[-1:]

  return links


def get_mentions_for_link_state(link, node_wise):
  link_split = link.split('->')

  if node_wise and len(link_split) == 1:
    m0 = link_split[0].strip()
    # print('link has only one mention?', link, m0)
    return [m0]

  elif len(link_split) < 2:
    print('link has only one mention - skipping mention', link)
    return []

  if len(link_split) > 2:
    print('link has too many mentions - using first two.', link)
  m0 = link_split[0].strip()
  m1 = link_split[1].strip()
  return [m0, m1]


# use mt5 and large context

class State(object):
  """Document state."""

  def __init__(self, input_document, node_wise=True, max_len_doc=3000):
    """ Create State object to process documents.

    Args:
      input_document: dictonary with the input document.
      node_wise: Predict mentions too.
      max_len_doc: max sentence pieace tokens, eg. 2000 or 3000 (bit better).

    """
    self.sentence_num = -1
    self.clusters_num = 0

    self.token_map_context, self.annotation_context = [], []
    self.annotation_coreference_start, self.annotation_coreference_end = [], []
    self.token_map, self.annotation = [], []

    # a mention index to cluster mapping, e.g. (23, 24) -> [(23, 24), (41, 42)]
    self.mention_index_to_cluster = {}

    # the first link names the cluster, e.g. (23, 24) -> '1'
    self.mention_index_to_cluster_name = {}
    self.cluster_name_to_cluster = {}

    self.input_document = input_document
    # print('sentence_num', self.sentence_num)
    self.genre = input_document['genres'][0][0]
    self.speakers = {t: spk for (t, spk) in self.input_document['speakers']}

    self.done = False
    self.predictions_str = {}  # keep the predictions
    self.node_wise = node_wise

    self.max_len_doc = max_len_doc

    # move to initial position.
    self.extend()


  def extend_done(self):
    return self.done

  def extend(self, prediction_str=None, use_gold_cluster=False, move=True):

    # move annotation to context
    self.token_map_context +=  self.token_map
    self.annotation_context += self.annotation

    for k in range(len(self.annotation)):
      self.annotation_coreference_start.append([])
      self.annotation_coreference_end.append([])

    assert len(self.annotation_context)  == len(self.annotation_coreference_start)

    self.annotation, self.token_map = [], []

    link_found = False
    if prediction_str is not None and not 'None [' in prediction_str:
      links = [l for l in prediction_str.split(';;') if l != '' ]

      annotation_update = []
      for link in links:
        link_found = True
        link_mentions = get_mentions_for_link_state(link, self.node_wise)

        if len(link_mentions) < 2 and not (self.node_wise and len(link_mentions)):
          print('less mentions as needed skip', link_mentions)
          continue
        indices = match_link_state(link_mentions, self.annotation_full,
                                   self.annotation_full_map,
                                   self.cluster_name_to_cluster,
                                   debug=False)

        if not indices:
          print('not found !!')
          print('indices not found', link, indices)
          print('self.annotation_full', self.annotation_full )
          print('annotation + context', self.get_input_annotation())
          continue

        if True:
          index = indices[0]
          cluster = []
          for mention_index in index:
            if str(mention_index) in self.mention_index_to_cluster:
              cluster = self.mention_index_to_cluster[str(mention_index)]
              break


          if not cluster:
            self.clusters_num += 1
            cluster_name = str(self.clusters_num)

            if use_gold_cluster:  # just to evaluate on gold

              for ni, cx in enumerate(self.input_document['clusters']):
                for mx in cx:
                  if mx in index:
                    cluster_name = str(ni+1)
                    break

          else:
            cluster_name = self.mention_index_to_cluster_name[str(cluster[0])]

          for mention_index in index:
            if mention_index not in cluster:
              cluster.append(mention_index)
              self.mention_index_to_cluster[str(mention_index)] = cluster
              self.cluster_name_to_cluster['['+cluster_name] = cluster
              self.mention_index_to_cluster_name[str(mention_index)] = cluster_name
              annotation_update.append([mention_index, cluster_name])

      # update the annotation
      if True:
        for update in annotation_update:
          update_index = update[0]
          update_name = update[1]

          for t, coref_starts, coref_end, tid in zip(self.annotation_context,
                                    self.annotation_coreference_start,
                                    self.annotation_coreference_end,
                                    self.token_map_context):



            if update_index[0] == tid:
              coref_starts.append(update)
              coref_starts.sort( key=lambda x: x[0][1], reverse=True)


            if update_index[1] == tid:
              coref_end.append(']')

    if move or 'None [' in prediction_str or not link_found:
      self.sentence_num += 1

      if self.sentence_num not in self.input_document['sentences']:
        self.done = True
        return True

      tokens = self.input_document['sentences'][self.sentence_num]
      token_map = self.input_document['token_maps'][self.sentence_num]
      first = True


      for tid, t in zip(token_map, tokens):
        if first:
          self.token_map.append(-1)
          speaker = normalize_speaker(self.speakers[tid])
          self.annotation.append(speaker)
          first = False
        self.token_map.append(tid)
        self.annotation.append(t)

    if self.sentence_num not in self.predictions_str:
      self.predictions_str[self.sentence_num] = ''

    if prediction_str is not None:
      self.predictions_str[self.sentence_num] += prediction_str

    return False

  def input_annotation(self):

    self.annotation_full = ['coref:', self.genre]
    self.annotation_full_map = [-1, -1]
    for t, coref_starts, coref_end, tid in zip(self.annotation_context,
                                  self.annotation_coreference_start,
                                  self.annotation_coreference_end,
                                  self.token_map_context):

      for coref_start in coref_starts:
        coref_name = coref_start[-1]

        self.annotation_full.append('[' + coref_name)
        self.annotation_full_map.append(-1)

      self.annotation_full.append(t)
      self.annotation_full_map.append(tid)

      for end in coref_end:
        coref_name = end[-1]
        self.annotation_full.append(coref_name)
        self.annotation_full_map.append(-1)

    self.annotation_full += ['|'] + self.annotation
    self.annotation_full_map += [-1] + self.token_map
    self.annotation_full += ['**']
    self.annotation_full_map += [-1]


  def encode(self, annotation_str):
    return tokenizer_mt5.encode(annotation_str)

  def get_input_annotation(self, context_right=True):

    self.input_annotation()
    annotation_str = ' '.join(self.annotation_full)

    enc = self.encode(annotation_str)
    shorten = len(enc) > self.max_len_doc

    while len(enc) > self.max_len_doc:   # inefficient ...
      self.annotation_context = self.annotation_context[1:]
      self.token_map_context = self.token_map_context[1:]
      self.annotation_coreference_start = self.annotation_coreference_start[1:]
      self.annotation_coreference_end = self.annotation_coreference_end[1:]

      self.input_annotation()
      annotation_str = ' '.join(self.annotation_full)
      enc = self.encode(annotation_str)

    last_token_id = self.annotation_full_map[-2]  # the last one is **
    self.annotation_context_right = []

    if not shorten and context_right:
      sentence_num = self.sentence_num
      total_len = len(enc)

      while True:
        sentence_num += 1
        if sentence_num not in self.input_document['sentences']:
          break

        first = True
        annotation_context_next = []

        for t, tid in zip(self.input_document['sentences'][sentence_num], self.input_document['token_maps'][sentence_num]):
          if first:
            speaker = normalize_speaker(self.speakers[tid])
            annotation_context_next.append(speaker)
            first = False
          annotation_context_next.append(t)

        annotation_context_right = self.annotation_context_right + annotation_context_next
        enc = self.encode(' '.join(annotation_context_right))

        if (len(enc) + total_len) > self.max_len_doc:
          break
        self.annotation_context_right = annotation_context_right
      if self.annotation_context_right:
        annotation_str = annotation_str + ' ' + ' '.join(self.annotation_context_right)

    enc = self.encode(annotation_str)
    if len(enc) > self.max_len_doc:
      print('warning: document too long', len(enc))

    return annotation_str


# @title function def to reate a input state
tokenizer_nltk = nltk.WordPunctTokenizer()


def create_document(document: str, title: str = 'not_named'):
  """Creates a datastructure with a title and uses nltk for tokenization.

  Args:
    document: sentences separated with newline ('\n').
    title: the name of the document.

  Returns:
    dict with sentences, maps to token-ids, speakers, and genres.
  """
  input_document = {
      'doc_key': title,
      'sentences': {},
      'token_maps': {},
      'speakers': [],
      'genres': []
  }

  tid = 0
  for k, sentence in enumerate(document.split('\n')):
    input_document['sentences'][k] = tokenizer_nltk.tokenize(text=sentence)
    input_document['token_maps'][k] = []

    for _ in input_document['sentences'][k]:
      input_document['token_maps'][k].append(tid)
      input_document['speakers'].append((tid, '_'))
      input_document['genres'].append('wi')
      tid += 1
  return input_document

# @title function def to create batches
def create_next_batch(states_dict, batche_size=1, num_batches=1):
  batches = [[]]
  states = []
  for key, state in states_dict.items():
    if state.extend_done():
      continue

    states.append(state)
    if len(states) >= (batche_size * num_batches):
      break
  for state in states:
    batches[-1].append(state.get_input_annotation())
    if len(batches[-1]) >= batche_size:
      if len(batches) >= num_batches:
        break
      batches.append([])
  return states, batches

titles = ["Eiffel Tower Wiki", "Pyramid of Giza Wiki","Colossus of Rhodes Wiki", "Gardens of Babylon Wiki", "Lighthouse of Alexandria Wiki", "Temple of Artemis Wiki"]

input_samples = [
    """The Eiffel Tower (French: tour Eiffel) is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.
Locally nicknamed "La dame de fer" (French for "Iron Lady"), it was constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair.
Although initially criticised by some of France's leading artists and intellectuals for its design, it has since become a global cultural icon of France and one of the most recognisable structures in the world.
The Eiffel Tower is the most visited monument with an entrance fee in the world: 6.91 million people ascended it in 2015.
It was designated a monument historique in 1964, and was named part of a UNESCO World Heritage Site ("Paris, Banks of the Seine") in 1991.""",
    
"""The Great Pyramid of Giza is the largest Egyptian pyramid and served as the tomb of pharaoh Khufu, who ruled during the Fourth Dynasty of the Old Kingdom.
Built in the early 26th century BC, over a period of about 27 years, the pyramid is the oldest of the Seven Wonders of the Ancient World, and the only wonder that has remained largely intact.
It is the most famous monument of the Giza pyramid complex, which is part of the UNESCO World Heritage Site "Memphis and its Necropolis".
It is situated at the northern end of the line of the three pyramids at Giza.""",

"""The Colossus of Rhodes (Ancient Greek: ὁ Κολοσσὸς Ῥόδιος, romanized: ho Kolossòs Rhódios; Greek: Κολοσσός της Ρόδου, romanized: Kolossós tes Rhódou) was a statue of the Greek sun god Helios, erected in the city of Rhodes, on the Greek island of the same name, by Chares of Lindos in 280 BC.
One of the Seven Wonders of the Ancient World, it was constructed to celebrate the successful defence of Rhodes city against an attack by Demetrius I of Macedon, who had besieged it for a year with a large army and navy.
According to most contemporary descriptions, the Colossus stood approximately 70 cubits, or 33 metres (108 feet) high – approximately the height of the modern Statue of Liberty from feet to crown – making it the tallest statue in the ancient world.
It collapsed during the earthquake of 226 BC, although parts of it were preserved.
In accordance with a certain oracle, the Rhodians did not rebuild it.
John Malalas wrote that Hadrian in his reign re-erected the Colossus, but he was mistaken.
According to the Suda, the Rhodians were called Colossaeans (Κολοσσαεῖς), because they erected the statue on the island.""",

"""The Hanging Gardens of Babylon were one of the Seven Wonders of the Ancient World listed by Hellenic culture.
They were described as a remarkable feat of engineering with an ascending series of tiered gardens containing a wide variety of trees, shrubs, and vines, resembling a large green mountain constructed of mud bricks.
It was said to have been built in the ancient city of Babylon, near present-day Hillah, Babil province, in Iraq.
The Hanging Gardens' name is derived from the Greek word κρεμαστός (kremastós, lit. 'overhanging'), which has a broader meaning than the modern English word "hanging" and refers to trees being planted on a raised structure such as a terrace.
According to one legend, the Hanging Gardens were built alongside a grand palace known as The Marvel of Mankind, by the Neo-Babylonian King Nebuchadnezzar II (who ruled between 605 and 562 BC), for his Median wife, Queen Amytis, because she missed the green hills and valleys of her homeland.
This was attested to by the Babylonian priest Berossus, writing in about 290 BC, a description that was later quoted by Josephus.
The construction of the Hanging Gardens has also been attributed to the legendary queen Semiramis and they have been called the Hanging Gardens of Semiramis as an alternative name.""",

"""The Lighthouse of Alexandria, sometimes called the Pharos of Alexandria (/ˈfɛərɒs/ FAIR-oss; Ancient Greek: ὁ Φάρος τῆς Ἀλεξανδρείας, romanized: ho Pháros tês Alexandreías, contemporary Koine Greek pronunciation: [ho pʰáros tɛ̂ːs aleksandrěːaːs]; Arabic: فنار الإسكندرية), was a lighthouse built by the Ptolemaic Kingdom of Ancient Egypt, during the reign of Ptolemy II Philadelphus (280–247 BC).
It has been estimated to have been at least 100 metres (330 ft) in overall height.
One of the Seven Wonders of the Ancient World, for many centuries it was one of the tallest man-made structures in the world.
The lighthouse was severely damaged by three earthquakes between 956 and 1323 AD and became an abandoned ruin.
It was the third-longest surviving ancient wonder, after the Mausoleum at Halicarnassus and the extant Great Pyramid of Giza, surviving in part until 1480, when the last of its remnant stones were used to build the Citadel of Qaitbay on the site.""",

"""The Temple of Artemis or Artemision (Greek: Ἀρτεμίσιον; Turkish: Artemis Tapınağı), also known as the Temple of Diana, was a Greek temple dedicated to an ancient, local form of the goddess Artemis (identified with Diana, a Roman goddess).
It was located in Ephesus (near the modern town of Selçuk in present-day Turkey).
By 401 AD it had been ruined or destroyed.[1] Only foundations and fragments of the last temple remain at the site.
The earliest version of the temple (a Bronze Age temenos) antedated the Ionic immigration by many years.
Callimachus, in his Hymn to Artemis, attributed it to the Amazons.
In the 7th century BC, it was destroyed by a flood.
Its reconstruction, in more grandiose form, began around 550 BC, under Chersiphron, the Cretan architect, and his son Metagenes.
The project was funded by Croesus of Lydia, and took 10 years to complete.
This version of the temple was destroyed in 356 BC by an arsonist."""]

states_dict = {titles[i]: State(create_document(input_samples[i], titles[i])) for i in range(6)}

emulate_predictions = False # @param

if emulate_predictions:
  predictioned_results = [
      [
          'It ## is named after -> The Eiffel Tower ( French : tour Eiffel ) ##'
          ' is a wrought ;; the tower ## . ** _ -> It ## is named after ;;'
      ],
      ['it ## was constructed from -> [1 ;;'],
      [
          'its ## design , it -> [1 ;; it ## has since become -> its ## design'
          " , it ;; France ' s ## leading artists and -> France ## . [1 It ;;"
          " France ## and one of -> France ' s ## leading artists and ;;"
      ],
      [
          'The Eiffel Tower ## is the most -> [1 ;; it ## in 2015 . -> The'
          ' Eiffel Tower ## is the most ;; the world ## : 6 . -> the world ## .'
          ' | _ ;;'
      ],
      [
          'It ## was designated a -> [1 ;; Paris ## , Banks of -> Paris , [2'
          ' France ## ] . [1 ;;'
      ],
  ]
else:
  predictioned_results = []

expand_only = False
total_time = time.time()
total_results = 0

debug = True

for step in range(4):  # while states
  t = time.time()
  states, batches = create_next_batch(states_dict, batche_size=2, num_batches=3)
  print(f"Step: {step}")

  if not states:
    print("No States")
    break

  print(f"States shape: 1x{len(states)}")
  print(f"Batches shape: {len(batches)}x{len(batches[0])}")

  documents_processing = set([x.input_document['doc_key'] for x in states])

  print(f'Processing documents: {documents_processing}')

  if predictioned_results:
    results = predictioned_results[step]
  else:
    predictions = predict_coreferences(batches, len(batches))
    print(f"Predictions shape: {len(predictions)}x{len(predictions[0])}")
    results = extract_result_string(predictions)
    print(f"Results shape: 1x{len(results)}")

  for state, result, batch in zip(states, results, batches):
    print(state, result, batch)
    state.extend(result)

    #if debug:
    #  print('input batch[0]: ', batch)
    #  print('mt5 output:     ', results)

  total_results += len(results)
  print(
      f'time { time.time()-t}, round time/seq : {(time.time()-t)/len(results)}'
      f' total time/seq: {(time.time()-total_time)/total_results}'
  )
  print()

# @title get and print the output as annotated document

for doc_name, s in states_dict.items():
  pred_clusters = [cluster for name, cluster in s.cluster_name_to_cluster.items()]
  print('predicted clusters with word indexes', pred_clusters)

  text, text_map = [], []
  for k, snt in states_dict[doc_name].input_document['sentences'].items():
    m = states_dict[doc_name].input_document['token_maps'][k]
    text += snt
    text_map += m

  cluster_annotations_start = []
  cluster_annotations_end = []

  # Cluster annotation per token
  for tid in text_map:
    cluster_annotations_start.append([])
    cluster_annotations_end.append([])
    for ci in pred_clusters:
      for m in ci:

        if tid == m[0]:
          m_len = m[1] - m[0]
          name = s.mention_index_to_cluster_name[str(m)]
          cluster_annotations_start[-1].append((name, m_len))

        if tid == m[1]:
          cluster_annotations_end[-1].append(']')

  # get the text with the coreference annotations
  all_text = []
  for tok, start, end in zip(text, cluster_annotations_start, cluster_annotations_end):

    if start:
      for x in sorted(start, key=lambda x : x[1], reverse=True):
        all_text.append('['+str(x[0]))

    all_text.append(tok)

    if end:
      all_text.append(''.join(end))

  print(' '.join(all_text))