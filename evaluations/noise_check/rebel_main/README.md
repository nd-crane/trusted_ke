# Rebel Main Noise Check

From here:

python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119 -i c5 -o c119.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_strip -i c5 -o c119_strip.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_spaceafter -i c5 -o c119_spaceafter.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_leadapost -i c5 -o c119_leadapost.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_leadtrailapost -i c5 -o c119_leadtrailapost.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_lowerletter -i c5 -o c119_lowerletter.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_lowerword -i c5 -o c119_lowerword.csv
python ../../../re/rebel/rebel_main.py -d ../sampled_noisy.csv -t c119_lower -i c5 -o c119_lower.csv

cd ..

python check_diff.py -d rebel_main -c head/relation/tail

Then view diff.csv