from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# tokenizer = AutoTokenizer.from_pretrained("Celestinian/TopicGPT")
# model = AutoModelForCausalLM.from_pretrained("Celestinian/TopicGPT")

def generate_text(prompt, temperature=0.1, max_size=20):
    input_ids = tokenizer.encode("#CONTEXT# " + prompt + " #TOPIC#", return_tensors='pt')
    input_ids = input_ids
    model.eval()

    output_tokens = []
    eos_token_id = tokenizer.encode('#')[0]

    for _ in range(max_size):
        with torch.no_grad():
            outputs = model(input_ids)
        logits = outputs.logits[:, -1, :] / temperature
        next_token = torch.multinomial(torch.softmax(logits, dim=-1), num_samples=1)
        if next_token.item() == eos_token_id:
            break
        input_ids = torch.cat((input_ids, next_token), dim=-1)
        output_tokens.append(next_token.item())

    output = tokenizer.decode(output_tokens)
    clean_output = output.replace('\n', '')
    return clean_output

if __name__ == "__main__":
    text = 'After the sound and the fury, weeks of demonstrations and anguished calls for racial justice, the man whose death gave rise to an international movement, and whose last words — “I can’t breathe” — have been a rallying cry, will be laid to rest on Tuesday at a private funeral in Houston.George Floyd, who was 46, will then be buried in a grave next to his mother’s.The service, scheduled to begin at 11 a.m. at the Fountain of Praise church, comes after five days of public memorials in Minneapolis, North Carolina and Houston and two weeks after a Minneapolis police officer was caught on video pressing his knee into Mr. Floyd’s neck for nearly nine minutes before Mr. Floyd died. That officer, Derek Chauvin, has been charged with second-degree murder and second-degree manslaughter. His bail was set at $1.25 million in a court appearance on Monday. The outpouring of anger and outrage after Mr. Floyd’s death — and the speed at which protests spread from tense, chaotic demonstrations in the city where he died to an international movement from Rome to Rio de Janeiro — has reflected the depth of frustration borne of years of watching black people die at the hands of the police or vigilantes while calls for change went unmet.'
    # preds = generate_text(text)
    # print(preds)
    print(text)