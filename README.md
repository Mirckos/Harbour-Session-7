# Harbour Space Session 7

Presentation and code examples for a Production ML lesson about fast UI MVPs with
Streamlit and Gradio.

## Environment

Use Python 3.10-3.13 for the ML demos:

```bash
python -m pip install -r requirements.txt
```

The local machine may have Python 3.14 already, but some ML wheels can lag behind
new Python releases.

## Run Examples

Streamlit:

```bash
streamlit run 01_streamlit_hello.py
streamlit run 04_streamlit_mini_dashboard.py
```

Gradio:

```bash
python 05_gradio_interface_hello.py
python 08_gradio_toxic_classifier.py
```

Gradio public sharing is off by default for safer local demos. Enable it only when
you need a public tunnel:

```bash
GRADIO_SHARE=true python 08_gradio_toxic_classifier.py
```

API client demo:

```bash
GRADIO_URL=http://127.0.0.1:7860 python 09_rest_api_test.py
```
