# Flair Noise Check

From here:

python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119 -i c5 -o c119.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_strip -i c5 -o c119_strip.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_spaceafter -i c5 -o c119_spaceafter.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_leadapost -i c5 -o c119_leadapost.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_leadtrailapost -i c5 -o c119_leadtrailapost.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_lowerletter -i c5 -o c119_lowerletter.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_lowerword -i c5 -o c119_lowerword.csv
python ../../../ner/flair/flair_ner.py -d ../sampled_noisy.csv -t c119_lower -i c5 -o c119_lower.csv

cd ..

python check_diff.py -d flair -c entities/labels

Then view diff.csv