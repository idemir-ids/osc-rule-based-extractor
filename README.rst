💬 Important

On June 26 2024, Linux Foundation announced the merger of its financial services umbrella, the Fintech Open Source Foundation (`FINOS <https://finos.org>`_), with OS-Climate, an open source community dedicated to building data technologies, modelling, and analytic tools that will drive global capital flows into climate change mitigation and resilience; OS-Climate projects are in the process of transitioning to the `FINOS governance framework <https://community.finos.org/docs/governance>`_; read more on `finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg <https://finos.org/press/finos-join-forces-os-open-source-climate-sustainability-esg>`_


========================
osc-rule-based-extractor
========================


.. image:: https://img.shields.io/badge/OS-Climate-blue
  :alt: An OS-Climate Project
  :target: https://os-climate.org/

.. image:: https://img.shields.io/badge/slack-osclimate-brightgreen.svg?logo=slack
  :alt: Join OS-Climate on Slack
  :target: https://os-climate.slack.com

.. image:: https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white
  :alt: Source code on GitHub
  :target: https://github.com/idemir-ids/osc-rule-based-extractor

.. image:: https://img.shields.io/pypi/v/osc-rule-based-extractor.svg
  :alt: PyPI package
  :target: https://pypi.org/project/osc-rule-based-extractor/

.. image:: https://api.cirrus-ci.com/github/os-climate/osc-rule-based-extractor.svg?branch=main
  :alt: Built Status
  :target: https://cirrus-ci.com/github/os-climate/osc-rule-based-extractor

.. image:: https://img.shields.io/badge/PDM-Project-purple
  :alt: Built using PDM
  :target: https://pdm-project.org/latest/

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
  :alt: Project generated with PyScaffold
  :target: https://pyscaffold.org/

Overview
--------

| Deterministic, rule-based PDF extractor using a modified XPDF
  pdftohtml binary (pdftohtml_mod).
| Converts raw PDFs into structured artifacts (e.g., HTML/XML/JSON and
  related intermediate files) using a reproducible pipeline.
| To be used for extracting KPIs from tables; complements ML-based text
  extractors.

Prerequisites
-------------

| **OS:** Linux (commands assume bash)
| **Python:** 3.12
| **System packages typically required:**
| ``git``, ``python3.12-venv``
| ``software-properties-common``, ``wget`` ``gfortran``,
  ``libopenblas-dev``, ``liblapack-dev``
| ``libpng-dev``, ``libfreetype-dev``, ``libfontconfig``
| ``libpng12`` (often not present by default on newer distros; see
  install notes)
| **Disk space:** enough for PDFs, working intermediates, and outputs

Installation (from GitHub using PDM)
------------------------------------

The steps below replicate the install process you provided, adjusted to
a general project layout.

1. Install system dependencies (requires sudo/root on typical setups)
   **Note:** ``libpng12`` may be required for ``pdftohtml_mod`` on some
   distributions.

::

   sudo apt-get update
   sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
   sudo apt-get install -qq git python3.12-venv software-properties-common \
     wget gfortran libopenblas-dev liblapack-dev libpng-dev libfreetype-dev libfontconfig

2. Install ``libpng12`` (ensure compatibility with your distro)
   The URL below is one example; check your OS for a compatible package.

::

   wget http://ppa.launchpad.net/linuxuprising/libpng12/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~eoan_amd64.deb
   sudo dpkg -i libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~eoan_amd64.deb

3. Clone dependencies

::

   git clone --quiet https://github.com/idemir-ids/osc-xpdf-mod
   git clone --quiet https://github.com/idemir-ids/osc-rule-based-extractor

4. Create and activate a dedicated virtual environment

::

   python3.12 -m venv venv_rb

5. Ensure the modified pdftohtml is executable
   **Note:** Depending on your distribution, you might need to build the
   pdftohtml_mod tool on your own. Please refer to its git repository
   for instructions.

::

   chmod +x osc-xpdf-mod/bin/pdftohtml_mod

6. Install Python dependencies with PDM

::

   source venv_rb/bin/activate
   cd osc-rule-based-extractor
   pip install --upgrade pip
   pip install pdm
   pdm sync
   cd ..
   deactivate

Demo folder structure To keep consistency with your other tools, use a demo folder layout:
------------------------------------------------------------------------------------------

::

   your-project/
   ├─ venv_rb/                      # Python venv for rule-based extractor
   ├─ osc-xpdf-mod/
   │  └─ bin/
   │     └─ pdftohtml_mod           # modified XPDF binary
   ├─ osc-rule-based-extractor/     # rule-based extractor repo
   └─ demo/
      └─ rulebased/
         ├─ input/                  # raw PDFs go here
         ├─ work/                   # working (intermediate) files
         ├─ output/                 # final extracted artifacts
         └─ log/                    # logs

Create demo folders and add PDFs:

::

   mkdir -p demo/rulebased/input demo/rulebased/work demo/rulebased/output demo/rulebased/log

Place your PDFs into demo/rulebased/input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Demo materials**

If you want to use the demo inputs that ship with the repo:

Clone just to copy demo inputs (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   git clone https://github.com/os-climate/osc-transformer-presteps.git

Copy demo inputs
^^^^^^^^^^^^^^^^

::

   cp -r osc-transformer-presteps/demo/extraction/input demo/rulebased

Quickstart
----------

Run the extractor against the demo folders:

1. Activate environment

::

   source venv_rb/bin/activate

2. Run rule-based extraction

::

   osc-rule-based-extractor \
     --pdftohtml_mod_executable "osc-xpdf-mod/bin/pdftohtml_mod" \
     --raw_pdf_folder "demo/rulebased/input" \
     --working_folder "demo/rulebased/work" \
     --kpi_folder "osc-rule-based-extractor/res/kpi_specs_demo" \
     --output_folder "demo/rulebased/output" \
     --verbosity 0 \
     > "demo/rulebased/log/rb.log"

3. Deactivate environment

::

   deactivate

Command reference
-----------------

::

   osc-rule-based-extractor \
     --pdftohtml_mod_executable <path_to_pdftohtml_mod> \
     --raw_pdf_folder <input_pdf_dir> \
     --working_folder <work_dir> \
     --kpi_folder "<kpi_folder>" \
     --output_folder <output_dir> \
     --verbosity <level>

Arguments:
----------

| **--pdftohtml_mod_executable:** absolute or relative path to the
  modified pdftohtml binary (pdftohtml_mod).
| **--raw_pdf_folder:** directory containing source PDF files.
| **--working_folder:** directory for intermediate artifacts
  (created/used by the pipeline).
| **--kpi_folder:** directory where KPI definition files are stored
| **--output_folder:** directory where final extracted outputs are
  written.
| **--verbosity:** integer log level (e.g., 0 for minimal output).

Outputs
-------

| The tool writes its final artifacts to the specified output folder.
| Depending on configuration and document content, outputs can include
  structured representations derived from the PDFs (e.g., HTML/XML/JSON
  files) and may rely on intermediates created in the working folder.
| The log file (e.g., demo/rulebased/log/rb.log) captures the run
  details.

Integration notes
-----------------

| This tool is complementary to ML-based workflows
  (osc-transformer-presteps and osc-transformer-based-extractor). If you
  plan to feed outputs downstream, ensure format compatibility and any
  required conversion steps.
| For consistency across your pipeline:
| Keep raw PDFs under ``demo/rulebased/input``.
| Maintain working intermediates under ``demo/rulebased/work``.
| Place final exports under ``demo/rulebased/output``.
| Store logs under ``demo/rulebased/log``.

Troubleshooting
---------------

| **pdftohtml_mod not executable:**
| Run ``chmod +x /path/to/pdftohtml_mod`` and ensure the path matches
  ``--pdftohtml_mod`` executable, or you might need to compile this
  binary on your OS.
| **Missing libpng12 or incompatible version:**
| Install a distro-compatible ``libpng12`` package. The example URL
  provided targets a specific Ubuntu release; adjust for your OS.
| **Font or layout issues:**
| Ensure ``libfreetype-dev`` and ``libfontconfig`` are installed.
  **Performance and memory:**
| Large PDFs can create big intermediate files. Ensure sufficient disk
  space in the working folder.
| **Logs:**
| Increase ``--verbosity`` for debugging, and remove ``2>/dev/null`` if
  you need stderr output in the log.

Best practices
--------------

| Use absolute paths for the ``pdftohtml_mod`` executable and folders
  when scripting long runs.
| Keep a clean working_folder to avoid mixing intermediates from
  previous runs.
| Version-control your extraction configs and environment setup scripts
  for reproducibility.

License and governance
----------------------

This tool is part of the broader OS-Climate ecosystem. Refer to the
``osc-rule-based-extractor`` repository for license, contribution, and
governance details.

