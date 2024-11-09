from routing.router import Redirect, Route

Route.cache_form = True


class HomeRoute(Route):
    path = "/"

    def before_load(self, **loader_args):
        raise Redirect(path="/books")


class BookRoute(Route):
    path = "/books"
    form = "forms.pages.book.Index"

    def cache_deps(self, **loader_args):
        return None


class AuthorRoute(Route):
    path = "/authors"
    form = "forms.pages.author.Index"

    def cache_deps(self, **loader_args):
        return None
