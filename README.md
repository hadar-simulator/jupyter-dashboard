# jupyter-dashboard

Jupyter Dashboard repo provides `hadar_dashboard` python package which is an one-line jupyter widget to display a little dashboard and navigate into Hadar results.
![Screenshost](screenshot-dashboard.gif)

## Use it
``` python
plottting = hd.HTMLPlotting(...)

from hadar_dashboard import dashboard

dashboard(plotting)
```

## Start example
#### By Binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hadar-simulator/jupyter-dashboard/master?filepath=example%2FBegin%20Stochastic.ipynb)

#### By yourself
```
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
jupyter notebook example/Begin\ Stochastic.ipynb
 
```
