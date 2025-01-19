from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Footer, Header, Static, DataTable
from textual.screen import ModalScreen
from textual.containers import Horizontal, Container
from textual.validation import Regex

from datatools import (add_book, 
                       remove_book, 
                       engine, 
                       check_title_exists,
                       get_all_data)


class AddBook(ModalScreen):

    def compose(self) -> ComposeResult:
        self.txt = Static()
        with Container():
            yield self.txt
            yield Input(placeholder="Title", id="input_title", validators=[Regex(".+")])
            yield Input(placeholder="Author", id="input_autor")
            yield Input(placeholder="Genre", id="input_genre")
            yield Input(placeholder="Veröffentlicht am", id="input_published")
            with Horizontal():
                yield Button("Hinzufügen", "success", id="confirm")
                yield Button("Abbrechen", "error", id="abort")

    def on_button_pressed(self, event:Button.Pressed):
        if event.button.id == 'confirm':
            title = self.query_one("#input_title", Input)
            author = self.query_one("#input_autor", Input)
            genre = self.query_one("#input_genre", Input)
            published = self.query_one("#input_published", Input)

            if title.is_valid:
                exists = check_title_exists(engine, title.value)
                if not exists:
                    result = add_book(engine, title.value, genre.value, author.value, published.value)
                    if not result: 
                        self.txt.update("Das hat nicht geklappt!")
                    else:
                        self.txt.update("Der Title wurde erfolgreich hinzugefügt!")
                        title.clear()
                        author.clear()
                        genre.clear()
                        published.clear()
                else:
                    self.txt.update("Der Title existiert bereits!")
            else:
                self.txt.update("Bitte gib ein Title ein!")
        if event.button.id == 'abort':
            self.action_exit()

    def action_exit(self):
        self.app.pop_screen()


class Library(App):

    CSS_PATH = "style.tcss"
    BINDINGS = [("ctrl+a", "add", "add a book"), 
                ("ctrl+r", "reload", "reload"),
                ("ctrl+d", "remove", "remove"),]

    row_selected = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self):
        table = self.query_one(DataTable)
        # bereinigt die komplette Tabelle
        table.clear(columns=True)
        table.add_columns(*("Title", "Author", "Genre", "Veröffentlicht"))
        table.add_rows(get_all_data(engine))
        table.cursor_type = "row"

    def action_add(self):
        self.push_screen(AddBook())

    def action_reload(self):
        self.on_mount()

    def action_remove(self):
        if len(self.row_selected) > 0:
            remove_book(engine, self.row_selected[0])
            self.on_mount()

    def on_data_table_row_selected(self, event:DataTable.RowSelected) -> list:
        table = self.query_one(DataTable)
        self.row_selected = table.get_row(event.row_key)


if __name__ == "__main__":
    app = Library()
    app.run()