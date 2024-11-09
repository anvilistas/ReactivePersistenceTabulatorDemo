from routing.router import Route, Redirect


class HomeRoute(Route):
    path = "/"

    def before_load(self, **loader_args):
        raise Redirect(path="/books")


class BookRoute(Route):
    path = "/books"
    form = "forms.pages.book.Index"


class AuthorRoute(Route):
    path = "/authors"
    form = "forms.pages.author.Index"
