# s2e-coref Results

The *_map columns are the raw output from s2e-coref. These columns contain dictionaries with the form {index of word in part of document: [index of coreference chain to which this word belongs]}

*Note:*
* "part of document" specifically refers to docs and parts in conll-12 formatted data. For faa.conll, each FAA data entry is a document with one part. Note that the word indices do not restart for each sentence in the part/FAA entry\
* "coreference chain" refers to words and phrases within the text which s2e-coref has identified to be "co-referring" (e.g., [pilot, he, his], [nose gear, gear])
* a single word can begin or end more than one span/phrase, and therefore be part of more than one coreference chain
* Each part of a coreference chain is either a single word (e.g. hangar), or a span with a start word and an end word (e.g. maintenance hangar, maintenance = start word, hangar = end word). Single words are denoted in word_map, and spans have their start words in start_map and their end words in end_map

*Example:*\
WHILE TAXIING TO MAINTENANCE HANGAR, PILOT LOST NOSE WHEEL STEERING. WINGTIP HIT HANGAR, CAUGHT ON FIRE.\
['while','taxiing','to','maintenance','hangar', ',', 'pilot','lost','nose','wheel','steering','.','wingtip','hit','hangar', ',', 'caught','on','fire,'.']\
start_map: {3:[0]}\
end_map: {4:[0]}\
word_map: {14:[0]}

**start_map** key: the index of a word at the start of a span, value: list of indices of coreference chains to which this span belongs.\
In this example, there is only one coreference chain, chain #0. The index 3 refers to 'maintenance'

**end_map** key: the index of a word at the end of a span, value: list of indices of coreference chains to which this span belongs.\
The index 3 refers to the 'hangar'. From this and the 3:[0] entry in start_map, we see that 'maintenance hanger' makes up a span in the coreference chain #0

**word_map** key: the index of a word, value: list of indices of coreference chains to which this word belongs.\
The index 14 refers to the second instance of 'hangar'. Since it belongs to coreference chain #0, we see that s2e-coref identified 'maintenance hangar' and 'hangar' as co-referring.

**corefs** This column contains the above information in a more readable form, created by our own code in s2e-coref/interpret_predictions.ipynb
