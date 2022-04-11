<h1 align="center">
  <br>
  <a href="http://autonom.io"><img src="https://raw.githubusercontent.com/autonomio/jako/main/assets/Jako-Logo-NoBg.png" alt="Jako" width="250"></a>
  <br>
</h1>

<h3 align="center">Parallelization of Hyperparameter Experiments with Talos</h3>

<p align="center">
  <a href="#jako">Jako</a> •
  <a href="#wrench-key-features">Key Features</a> •
  <a href="#arrow_forward-examples">Examples</a> •
  <a href="#floppy_disk-install">Install</a> •
  <a href="#speech_balloon-how-to-get-support">Support</a> •
  <a href="https://autonomio.github.io/talos/">Docs</a> •
  <a href="https://github.com/autonomio/talos/issues">Issues</a> •
  <a href="#page_with_curl-license">License</a> •
  <a href="https://github.com/autonomio/talos/archive/master.zip">Download</a>
</p>
<hr>
<p align="center">
Jako makes it straightforward to <strong>distribute Talos experiments</strong> across one or more remote machines without asking you to change anything in the way you are already working with Talos.
</p>

### Jako

Jako solves the problem of wanting to run a single Talos experiment on one or more remote machines:

  - Easily start distributed Talos experiments
  - Access experiment results in real-time through centralized datastore
  - Takes minutes to implement
  - No new syntax or anything else to learn
  - Adds no overhead to your current Talos workflow

Jako is built to work exclusively with [Talos](https://github.com/autonomio/talos).

<hr>

### :wrench: Key Features

- `jako.DistributedScan()` works exactly like `talos.Scan()`
- Distribute experiments across one or more remote machines
- Local machine can be included in the experiment
- Zero-configuration; add new machines simply by adding them to a config file
- Manage keys, passwords and other details in a single config file or a dictionary
- Optionally run `DistributedScan()` through `talos.DistributedScan()`

Jako works on **Linux, Mac OSX**, and **Windows** systems and can be operated cpu, gpu, and multi-gpu systems.

<hr>

### :arrow_forward: Examples

All of the below <strong>Talos</strong> examples will work, simply change `talos.Scan()` to `talos.DistributedScan()` or `jako.DistributedScan()` and you're good to go.

Get the below code [here](https://gist.github.com/mikkokotila/4c0d6298ff0a22dc561fb387a1b4b0bb). More examples further below.

<img src=https://i.ibb.co/VWd8Bhm/Screen-Shot-2019-01-06-at-11-26-32-PM.png>

The *Simple* example below is more than enough for starting to use Talos with any Keras model. *Field Report* has +2,600 claps on Medium because it's more entertaining.

[Simple](https://nbviewer.jupyter.org/github/autonomio/talos/blob/master/examples/A%20Very%20Short%20Introduction%20to%20Hyperparameter%20Optimization%20of%20Keras%20Models%20with%20Talos.ipynb)  [1-2 mins]

[Concise](https://nbviewer.jupyter.org/github/autonomio/talos/blob/master/examples/Hyperparameter%20Optimization%20on%20Keras%20with%20Breast%20Cancer%20Data.ipynb)  [~5 mins]

[Comprehensive](https://nbviewer.jupyter.org/github/autonomio/talos/blob/master/examples/Hyperparameter%20Optimization%20with%20Keras%20for%20the%20Iris%20Prediction.ipynb)  [~10 mins]

[Field Report](https://towardsdatascience.com/hyperparameter-optimization-with-keras-b82e6364ca53)  [~15 mins]

For more information on how Talos can help with your Keras, TensorFlow (tf.keras) and PyTorch workflow, visit the [User Manual](https://autonomio.github.io/talos/).

You may also want to check out a visualization of the [Talos Hyperparameter Tuning workflow](https://github.com/autonomio/talos/wiki/Workflow).

<hr>

### :floppy_disk: Install

Stable version:

#### `pip install jako`

Daily development version:

#### `pip install git+https://github.com/autonomio/jako`

<hr>

### :speech_balloon: How to get Support

| I want to...                     | Go to...                                                  |
| -------------------------------- | ---------------------------------------------------------- |
| **...troubleshoot**           | [Docs] · [GitHub Issue Tracker]                   |
| **...report a bug**           | [GitHub Issue Tracker]                                     |
| **...suggest a new feature**  | [GitHub Issue Tracker]                                     |
| **...get support**            | [Stack Overflow]                     |

<hr>

### :loudspeaker: Citations

If you use Talos for published work, please cite:

`Autonomio Talos with Jako [Computer software]. (2022). Retrieved from http://github.com/autonomio/jako.`

<hr>

### :page_with_curl: License

[MIT License](https://github.com/autonomio/jako/blob/main/LICENSE)

[github issue tracker]: https://github.com/autonomio/jako/issues
[docs]: https://autonomio.github.io/jako/
[stack overflow]: https://stackoverflow.com/questions/tagged/jako
