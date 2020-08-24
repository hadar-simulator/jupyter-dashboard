from ipywidgets import widgets, interactive_output
from IPython.display import display
import plotly.graph_objects as go

import hadar as hd


class Container:
    """
    Main component create tabs and plot inside
    """
    def __init__(self, tabs: widgets, plotting):
        self.tabs = tabs
        self.plotting = plotting

    def update(self, network: str, node: str, type: str, name: str):
        """
        Single public access. Specify user choice for plotting selection

        :param network: network name
        :param node: nodes name or None for all nodes
        :param type: types name between [Consumptions, Productions, Links] or None for all node elements
        :param name: element name
        :return:
        """
        if network is None:
          return
        elif node is None:
            self._network(network)
        elif type is None:
            self._node(network, node)
        elif name is not None:
            self._element(network, node, type, name)

    def _network(self, network: str):
        """
        Display network screen with RAC and Exchange tab.

        :return:
        """
        self.tabs.children = [self._rac(network), self._exchanges(network)]
        self.tabs.set_title(0, 'RAC')
        self.tabs.set_title(1, 'Exchange Map')

    def _rac(self, network: str):
        """
        Display RAC matrix.
        :param network: network name

        :return:
        """
        return go.FigureWidget(self.plotting.network(network).rac_matrix())

    def _exchanges(self, network: str):
        """
        Display Exchange matrix manage user interaction with time, scn and zoom sliders.
        :param network: network name

        :return:
        """
        def changes(time, scn, zoom):
            try:
                display(go.FigureWidget(self.plotting.network(network).map(t=time, scn=scn, zoom=zoom)))
            except ValueError:
                pass

        time = widgets.IntSlider(value=0, min=0, description='time', max=self.plotting.agg.horizon - 1,
                                 continuous_update=False, disabled=False)
        scn = widgets.IntSlider(value=0, min=0, description='scn', max=self.plotting.agg.nb_scn - 1,
                                continuous_update=False, disabled=False)
        zoom = widgets.FloatSlider(value=6, min=1, description='zoom', max=10, disabled=False)
        hbox = widgets.HBox([time, scn, zoom])

        inter = interactive_output(changes, {'time': time, 'scn': scn, 'zoom': zoom})
        return widgets.VBox([hbox, inter])

    def _node(self, network: str, node: str):
        """
        Display node screen with Stack tab.

        :param network: network name
        :param node: node names
        :return:
        """
        self.tabs.children = [self._stack(network, node)]
        self.tabs.set_title(0, 'Stack')

    def _stack(self, network: str, node: str):
        """
        Display stack graphics. Manage user interaction with scn slider and prod, cons choices.

        :param network: network name
        :param node: node name
        :return:
        """
        def changes(scn, prod, cons):
            display(go.FigureWidget(self.plotting.network(network).node(node).stack(scn=scn, prod_kind=prod, cons_kind=cons)))

        scn = widgets.IntSlider(value=0, min=0, description='scn', max=self.plotting.agg.nb_scn - 1,
                                continuous_update=False, disabled=False)
        cons = widgets.RadioButtons(options=['asked', 'given'], value='asked', description='Consumption')
        prod = widgets.RadioButtons(options=['avail', 'used'], value='used', description='Production')
        hbox = widgets.HBox([scn, cons, prod])

        inter = interactive_output(changes, {'scn': scn, 'prod': prod, 'cons': cons})
        return widgets.VBox([hbox, inter])

    def _element(self, network: str, node: str, types: str, name: str):
        """
        Display element screen with Timeline, Monotone and Gaussian tabs

        :param network: network name
        :param node: node name
        :param types: type name between [Consumptions, Productions, Links]
        :param name: element name
        :return:
        """
        if types == 'Storage':
            p = self.plotting.storage(node, name)
            self.tabs.children = [self.candles(p)]
            self.tabs.set_title(0, 'Candles')
            return

        elif types == 'Consumptions':
            p = self.plotting.network(network).node(node).consumption(name)
        elif types == 'Productions':
            p = self.plotting.network(network).node(node).production(name)
        elif types == 'Links':
            p = self.plotting.network(network).node(node).link(name)

        self.tabs.children = [self.timeline(p), self.monotone(p), self.gaussian(p)]
        self.tabs.set_title(0, 'Timeline')
        self.tabs.set_title(1, 'Monotone')
        self.tabs.set_title(2, 'Gaussian')

    def timeline(self, plot):
        """
        Plot timeline graphics.

        :param plot: PlotElement to use
        :return:
        """
        return go.FigureWidget(plot.timeline())

    def monotone(self, plot):
        """
        Plot monotone graphics manage user interactions with time and scn sliders.

        :param plot: PlotElement to use
        :return:
        """
        def change(choice, time_v, scn_v):
            if choice == 'time':
                scn.disabled = True
                time.disabled = False
                display(go.FigureWidget(plot.monotone(t=time_v)))
            if choice == 'scn':
                scn.disabled = False
                time.disabled = True
                display(go.FigureWidget(plot.monotone(scn=scn_v)))

        choice = widgets.RadioButtons(options=['time', 'scn'], value='time', description='')
        time = widgets.IntSlider(value=0, min=0, description='time', max=self.plotting.agg.horizon - 1,
                                 continuous_update=False, disabled=False)
        scn = widgets.IntSlider(value=0, min=0, description='scn', max=self.plotting.agg.nb_scn - 1,
                                continuous_update=False, disabled=True)
        hbox = widgets.HBox([choice, time, scn])

        inter = interactive_output(change, {'choice': choice, 'time_v': time, 'scn_v': scn})
        return widgets.VBox([hbox, inter])

    def gaussian(self, plot):
        """
        Plot gaussian graphics manage user interactions with time ans scn sliders

        :param plot: plotElement to use
        :return:
        """
        def change(choice, time_v, scn_v):
            if choice == 'time':
                scn.disabled = True
                time.disabled = False
                display(go.FigureWidget(plot.gaussian(t=time_v)))
            if choice == 'scn':
                scn.disabled = False
                time.disabled = True
                display(go.FigureWidget(plot.gaussian(scn=scn_v)))

        choice = widgets.RadioButtons(options=['time', 'scn'], value='time', description='')
        time = widgets.IntSlider(value=0, min=0, description='time', max=self.plotting.agg.horizon - 1,
                                 continuous_update=False, disabled=False)
        scn = widgets.IntSlider(value=0, min=0, description='scn', max=self.plotting.agg.nb_scn - 1,
                                continuous_update=False, disabled=True)
        hbox = widgets.HBox([choice, time, scn])

        inter = interactive_output(change, {'choice': choice, 'time_v': time, 'scn_v': scn})
        return widgets.VBox([hbox, inter])


def navbar(study: hd.Study, tabs: Container):
    """
    Display top navbar. Manage interaction with user to select study element to plot.

    :param study: study to use
    :param tabs: container object to call when update
    :return:
    """
    networks = widgets.Dropdown(options=list(study.networks.keys()),
                                description='Networks', disable=False)
    nodes = widgets.Dropdown(options=['All'],
                             value='All', description='Nodes', disabled=False)
    types = widgets.Dropdown(options=['Node', 'Consumptions', 'Productions', 'Links'],
                             value='Node', description='elements', disabled=True)
    names = widgets.Dropdown(options=['None'], value='None', description='Names', disabled=True)

    def networks_changes(state):
        if state['name'] == 'value' and state['type'] == 'change':
            nodes.options = ['All'] + list(study.networks[state['new']].nodes.keys())
            nodes_changes(dict(name='value', type='change', new=nodes.value))

    networks.observe(networks_changes)

    def nodes_changes(state):
        if state['name'] == 'value' and state['type'] == 'change':
            if state['new'] == 'All':
                types.disabled = True
                names.disabled = True
                tabs.update(network=networks.value, node=None, type=None, name=None)
            else:
                types.disabled = False
                types_changes(dict(name='value', type='change', new=types.value))

    nodes.observe(nodes_changes)

    def types_changes(state):
        if state['name'] == 'value' and state['type'] == 'change':
            if state['new'] == 'Node':
                names.disabled = True
                tabs.update(network=networks.value, node=nodes.value, type=None, name=None)
            else:
                if state['new'] == 'Consumptions':
                    el = [e.name for e in study.networks[networks.value].nodes[nodes.value].consumptions]
                elif state['new'] == 'Productions':
                    el = [e.name for e in study.networks[networks.value].nodes[nodes.value].productions]
                elif state['new'] == 'Links':
                    el = [e.name for e in study.networks[networks.value].nodes[nodes.value].links]
                names.options = el
                names.disabled = False
                names_changes(dict(name='value', type='change', new=names.value))

    types.observe(types_changes)

    def names_changes(state):
        if state['name'] == 'value' and state['type'] == 'change':
            tabs.update(network=networks.value, node=nodes.value, type=types.value, name=names.value)

    names.observe(names_changes)

    networks_changes(dict(name='value', type='change', new=networks.value))
    return widgets.HBox([networks, nodes, types, names])


def dashboard(plotting):
    """
    Entry point to display complete Dashboard.

    :param plotting: Plotting implementation to use.
    :return:
    """
    tabs = widgets.Tab()
    container = Container(tabs, plotting)
    nav = navbar(plotting.agg.study, container)
    return widgets.VBox([nav, tabs])
