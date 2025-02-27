# Reactive Persistence Tabulator Demo

This app is an experiment where we explore how best to integrate recent developments
within the Anvil ecosystem.

Our aims for this experiment are:

* To discover whether it is possible to integrate these various tools in a coherent
  useful manner
* To discover whether doing so brings any benefit either to the capability of the apps
  we build or the clarity of their codebase
* To identify patterns of code that emerge that could form re-usable components

# Components

The specific tools which we are investigating are:

From Anvil:

* The [Material 3 Theme](https://github.com/anvil-works/material-3-theme) - layouts, sidesheet and a bunch of nicely themed components
* The [Routing Dependency](https://github.com/anvil-works/routing) - url based routing that works both client and server side
* [Model Classes](https://anvil.works/docs/data-tables/model-classes) - Customisable data table row objects

From Ourselves (The [anvilistas team](https://github.com/anvilistas/)):

* The [Reactive Dependency](https://github.com/anvilistas/reactive) - signals for Anvil apps
* The [Tabulator Dependency](https://github.com/anvilistas/tabulator) - datagrid/repeating panel alternative

# A Note on Persistence

When this experiment first started, it included the [persistence module](https://anvil-extras.readthedocs.io/en/latest/guides/modules/persistence.html#)
from [Anvil Extras](https://github.com/anvilistas/anvil-extras). However, with the recent
release of Model Classes from Anvil, that module has been superseded and we have
migrated this app to use those Model Classes in place of any element from persistence.

We just haven't changed the name!
