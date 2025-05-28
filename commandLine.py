from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from api import BooksAPI
from manager import SaveLoad
from books import BookDir
class CLI:
    """
    Command Line Interface for the Book Search Tool.
    Handles user interaction, displays menus, and other actions.
    """
    def __init__(self, api_key=None):
        self.console = Console()
        self.api = BooksAPI(api_key=api_key)
        self.manager = SaveLoad()
        self.current_search_results = []
        self.top_results_per_page = 5

    def run(self):
        """
        Runs the main application loop, displaying the main menu.
        """
        while True:
            self.console.print(Panel("[bold yellow]Enoch's Mini Book Search CLI Tool[/bold yellow]", title_align="center", style="bold green"))
            self.console.print("[1] Search for books")
            self.console.print("[2] View saved books")
            self.console.print("[3] Exit")

            choice = self.console.input("[bold cyan]Enter your choice: [/bold cyan]").strip()

            if choice == '1':
                self.search_books_menu()
            elif choice == '2':
                self.view_saved_books_menu()
            elif choice == '3':
                self.console.print("[bold green]Exiting the application. Goodbye![/bold green]")
                break
            else:
                self.console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            self.console.print("\n")

    def search_books_menu(self):
        """
        Handles the book search functionality, prompts user for query,
        displays results, and offers to save books.
        """
        query = self.console.input("[bold magenta]Enter book title or author to search: [/bold magenta]").strip()
        if not query:
            self.console.print("[bold red]Search query cannot be empty.[/bold red]")
            return

        self.console.print(f"[bold blue]Searching for '{query}'...[/bold blue]")
        self.current_search_results = []
        start_index = 0

        while True:
            results = self.api.search_book(query, top_results=self.top_results_per_page, start_index=start_index)

            if not results and start_index == 0:
                self.console.print("[bold yellow]No books found matching your query.[/bold yellow]")
                break
            elif not results:
                self.console.print("[bold yellow]No more results found for your query.[/bold yellow]")
                break

            self.current_search_results.extend(results)
            self._display_search_results(results, start_index)

            action = self.console.input(
                "[bold cyan]Enter a number to save, 'n' for next page, or 'b' to go back: [/bold cyan]"
            ).strip().lower()

            if action == 'b':
                break
            elif action == 'n':
                start_index += self.top_results_per_page
                self.console.print("[bold blue]Fetching next page...[/bold blue]")
            else:
                try:
                    selected_index = int(action)
                    # Adjust index for the current page display
                    adjusted_index = selected_index - 1 - start_index
                    if 0 <= adjusted_index < len(results):
                        book_to_save = results[adjusted_index]
                        self.manager.save_book(book_to_save)
                    else:
                        self.console.print("[bold red]Invalid book number.[/bold red]")
                except ValueError:
                    self.console.print("[bold red]Invalid input. Please enter a number, 'n', or 'b'.[/bold red]")
                except IndexError:
                    self.console.print("[bold red]Book number out of range.[/bold red]")

    def _display_search_results(self, books, start_index):
        """
        Helper method to display search results in a formatted table.

        Args:
            books (list[BookDir]): List of Book objects to display.
            start_index (int): The starting index for numbering the results.
        """
        if not books:
            return

        table = Table(title=f"Search Results (Page from {start_index+1})", show_lines=True, box=box.ROUNDED)
        table.add_column("No.", style="cyan", justify="right")
        table.add_column("Title", style="green", no_wrap=False)
        table.add_column("Author(s)", style="magenta", no_wrap=False)
        table.add_column("Published Date", style="blue", justify="center")

        for i, book in enumerate(books):
            # Ensure we only display up to top_results_per_page
            if i >= self.top_results_per_page:
                break
            display_num = start_index + i + 1
            authors = ", ".join(book.authors) if book.authors else "N"
            table.add_row(
                str(display_num),
                book.title,
                authors,
                book.published_date
            )
        self.console.print(table)

    def view_saved_books_menu(self):
        """
        Displays all locally saved books.
        """
        saved_books = self.manager.load_books()
        if not saved_books:
            self.console.print("[bold yellow]No books saved yet.[/bold yellow]")
            return

        table = Table(title="Your Saved Books", show_lines=True, box=box.ROUNDED)
        table.add_column("No.", style="cyan", justify="right")
        table.add_column("Title", style="green", no_wrap=False)
        table.add_column("Author(s)", style="magenta", no_wrap=False)
        table.add_column("Published Date", style="blue", justify="center")
     

        for i, book in enumerate(saved_books):
            authors = ", ".join(book.authors) if book.authors else "N/A"
            # isbns_str = "\n".join([f"{isbn['type']}: {isbn['identifier']}" for isbn in book.isbns]) if book.isbns else "N/A"
            # description_text = Text(book.description, style="white")
            # if len(description_text.plain) > 150: # Truncate long descriptions
            #     description_text = Text(description_text.plain[:147] + "...", style="white")

            table.add_row(
                str(i + 1),
                book.title,
                authors,
                book.published_date,
            )
        self.console.print(table)