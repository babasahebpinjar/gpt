import json
import os

import gradio as gr
import requests

APIKEY = os.environ.get("APIKEY")
APISECRET = os.environ.get("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")


def predict(prompt, lang, seed, out_seq_length, temperature, top_k, top_p):
    global APIKEY
    global APISECRET

    if prompt == '':
        return 'Input should not be empty!'

    url = 'https://tianqi.aminer.cn/api/v2/multilingual_code_generate_block'

    payload = json.dumps({
        "apikey"        : APIKEY,
        "apisecret"     : APISECRET,
        "prompt"        : prompt,
        "lang"          : lang,
        "out_seq_length": out_seq_length,
        "seed"          : seed,
        "temperature"   : temperature,
        "top_k"         : top_k,
        "top_p"         : top_p,
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=(20, 100)).json()
    except Exception as e:
        return 'Timeout! Please wait a few minutes and retry'

    if response['status'] == 1:
        return response['message']

    answer = response['result']['output']['code'][0]

    return prompt + answer


def main():
    gr.close_all()
    examples = []
    with open("./example_inputs.jsonl", "r") as f:
        for line in f:
            examples.append(list(json.loads(line).values()))

    with gr.Blocks() as demo:
        gr.Markdown(
            """
            <img src="https://raw.githubusercontent.com/THUDM/CodeGeeX/main/resources/logo/codegeex_logo.png">
            """)
        gr.Markdown(
            """
            <p align="center">
                🏠 <a href="https://codegeex.cn" target="_blank">Homepage</a> | 📖 <a href="http://keg.cs.tsinghua.edu.cn/codegeex/" target="_blank">Blog</a> | 🪧 <a href="https://codegeex.cn/playground" target="_blank">DEMO</a> | 🛠 <a href="https://marketplace.visualstudio.com/items?itemName=aminer.codegeex" target="_blank">VS Code</a> or <a href="https://plugins.jetbrains.com/plugin/20587-codegeex" target="_blank">Jetbrains</a> Extensions | 💻 <a href="https://github.com/THUDM/CodeGeeX" target="_blank">Source code</a> | 🤖 <a href="https://models.aminer.cn/codegeex/download/request" target="_blank">Download Model</a>
            </p>
            """)
        gr.Markdown(
            """
            We introduce CodeGeeX, a large-scale multilingual code generation model with 13 billion parameters, pre-trained on a large code corpus of more than 20 programming languages. CodeGeeX supports 15+ programming languages for both code generation and translation. CodeGeeX is open source, please refer to our [GitHub](https://github.com/THUDM/CodeGeeX) for more details. This is a minimal-functional DEMO, for other DEMOs like code translation, please visit our [Homepage](https://codegeex.cn). We also offer free [VS Code](https://marketplace.visualstudio.com/items?itemName=aminer.codegeex) or [Jetbrains](https://plugins.jetbrains.com/plugin/20587-codegeex) extensions for full functionality. 
            """)

        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(lines=13, placeholder='Please enter the description or select an example input below.',label='Input')
                with gr.Row():
                    gen = gr.Button("Generate")
                    clr = gr.Button("Clear")

            outputs = gr.Textbox(lines=15, label='Output')

        gr.Markdown(
            """
            Generation Parameter
            """)
        with gr.Row():
            with gr.Column():
                lang = gr.Radio(
                    choices=["C++", "C", "C#", "Python", "Java", "HTML", "PHP", "JavaScript", "TypeScript", "Go",
                             "Rust",
                             "SQL", "Kotlin", "R", "Fortran"], value='lang', label='Programming Language',
                    default="Python")
            with gr.Column():
                seed = gr.Slider(maximum=10000, value=8888, step=1, label='Seed')
                with gr.Row():
                    out_seq_length = gr.Slider(maximum=1024, value=128, minimum=1, step=1, label='Output Sequence Length')
                    temperature = gr.Slider(maximum=1, value=0.2, minimum=0, label='Temperature')
                with gr.Row():
                    top_k = gr.Slider(maximum=40, value=0, minimum=0, step=1, label='Top K')
                    top_p = gr.Slider(maximum=1, value=1.0, minimum=0, label='Top P')

        inputs = [prompt, lang, seed, out_seq_length, temperature, top_k, top_p]
        gen.click(fn=predict, inputs=inputs, outputs=outputs)
        clr.click(fn=lambda value: gr.update(value=""), inputs=clr, outputs=prompt)

        gr_examples = gr.Examples(examples=examples, inputs=[prompt, lang],
                                  label="Example Inputs (Click to insert an examplet it into the input box)",
                                  examples_per_page=20)
        
    demo.launch()

if __name__ == '__main__':
    main()