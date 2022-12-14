from IPython.display import display, HTML, Markdown


class JupyterMixin:

    def display_obj(self, obj):
        display(obj)

    def render_text(self, text, text_type=None):
        if text_type in [f'h{r}' for r in range(1, 7)]:
            display(HTML(f"<{text_type}>{text}</{text_type}>"))
        else:
            print(text)

    def render_header_if_needed(self, state, header_text):
        sample_size = state.get('sample_size', None)
        if self.headers:
            sample_info = '' if sample_size is None else f' (sample size: {sample_size})'
            header = f'{header_text}{sample_info}'
            self.render_text(header, text_type='h3')

    def render_markdown(self, md):
        display(Markdown(md))
