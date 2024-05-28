# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")
model = AutoModelForMaskedLM.from_pretrained("google-bert/bert-base-cased")

save_directory = "."

# Save the tokenizer
tokenizer.save_pretrained(save_directory)

# Save the model
model.save_pretrained(save_directory)
