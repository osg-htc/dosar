# AI Tools for Physicists: An Introduction
## African School of Physics — Kenya 2026
### Exercise Documentation

---

## Background

You have just completed two distributed computing exercises:

1. **Mandelbrot set** — an embarrassingly parallel problem where each pixel is computed independently across many grid nodes
2. **Z→mumu dimuon analysis** — a data-parallel HEP analysis where the same code runs on different data chunks across the WLCG grid, and you combined results at the end to reconstruct the Z boson mass peak

These exercises share a fundamental architecture with modern AI:

Large Language Models (LLMs) like GPT and Claude are trained using **data parallelism** across thousands of GPUs. The same model code runs on different batches of training data simultaneously, and the results (gradients) are combined back to a central parameter server at the end of each training step. This is conceptually identical to your HTCondor jobs running on different data files and combining histograms at the end.

The difference is scale and hardware, not architecture.

---

## Exercise Overview

In this exercise you will use an AI assistant to help you write PyROOT plotting code for your Z→mumu analysis results. The AI acts as a knowledgeable coding collaborator — you describe what you want in plain English, and it generates complete, runnable PyROOT code with explanations. All work will be run on your local machine.

**Learning objectives:**

- Understand how an API call works (client → server → AI → response)
- Use AI as a tool for scientific coding tasks
- Practice iterative prompt engineering
- Understand the limits of AI-generated code
- Learn how to get your own free AI API access after the school

---

## The Architecture

When you run the script, this is what happens:

```
Your machine
    |
    | HTTP POST request (your question as JSON)
    |
    v
ASP proxy server (asp.travelwith.kids)
    |
    | Validated request with physics system prompt
    |
    v
Anthropic API (Claude Haiku)
    |
    | PyROOT code + explanation
    |
    v
ASP proxy server
    |
    | Response forwarded
    |
    v
Your machine (code printed to terminal)
```

This is the same client-server pattern used in production AI systems everywhere. The proxy server holds the API key so individual users never need their own credentials for the class exercise.

---

## Setup

The script requires only Python 3, which is already installed on your Scientific Linux VM. No additional packages are needed.

**Step 1 — Get the script**

Download the <a href="https://osg-htc.org/dosar/ASP2026/asp_assistant.py" download="asp_assistant.py">asp_assistant.py</a> file. 

**Step 2 — Set your class token**

Open the script in a text editor:

```bash
nano asp_assistant.py
```

Find this line near the top:

```python
CLASS_TOKEN = "replace_me"
```

Replace `replace_me` with the token written on the whiteboard. Save and close.

**Step 3 — Run it**

```bash
python asp_assistant.py
```

---

## Running the Exercise

### Step 1: Start with a basic plot

Run the assistant and describe your Z→mumu histogram. A good starting question:

```
I have a TH1F histogram called zMass containing the dimuon invariant
mass from my Z to mumu analysis. The range is 0 to 200 GeV. Please write
PyROOT code to plot it with proper axis labels and a title.
```

Copy the generated code into a new file called `plot_zmass.py` and run it in interactive mode:

```bash
python -i plot_zmass.py
```

### Step 2: Add a Gaussian fit

Ask the assistant to add a fit:

```
Now add a Gaussian fit to the Z peak. The peak should be around 91 GeV.
Also add a linear background term.
```

Or more specifically:

```
Add a TF1 fit with a Gaussian signal plus a first-order polynomial
background. Fit in the range 80 to 100 GeV. Print the fit parameters
and show them on the plot.
```

### Step 3: Iterate and improve

Try these follow-up requests one at a time:

- `Add the chi-squared per degree of freedom to the legend`
- `Change the histogram fill color to light blue with a dark blue border`
- `Add a vertical dashed line at 91.2 GeV to mark the PDG Z mass value`
- `Save the plot as a PDF file called zmass_fit.pdf`
- `Make the axis labels larger — font size 16`

### Step 4: Test the limits

Ask the AI something it cannot know:

```
Add error bars that show the systematic uncertainty from the energy scale calibration
```

The AI does not know your specific systematic uncertainties. Observe how it handles this — does it make up numbers? Does it ask for clarification? This is an important lesson: AI is a tool, not an oracle.

---

## Complete Working Example

```python
import ROOT

# Open your ROOT file and get the histogram
f = ROOT.TFile("histograms-z.root", "READ")
h_mmumu = f.Get("zMass")
h_mmumu.SetDirectory(0)  # Keep histogram in memory after file closes
f.Close()

# Style the histogram
h_mmumu.SetFillColor(ROOT.kAzure - 9)
h_mmumu.SetLineColor(ROOT.kAzure + 1)
h_mmumu.SetLineWidth(2)
h_mmumu.GetXaxis().SetTitle("m_{mumu} [GeV/c^{2}]")
h_mmumu.GetYaxis().SetTitle("Events / 1 GeV")
h_mmumu.GetXaxis().SetTitleSize(0.05)
h_mmumu.GetYaxis().SetTitleSize(0.05)
h_mmumu.SetTitle("Z #rightarrow mumu Invariant Mass")

# Define fit function: Gaussian signal + linear background
fit_func = ROOT.TF1("fit_func",
    "[0]*TMath::Gaus(x,[1],[2]) + [3] + [4]*x",
    80, 100)

# Set initial parameter values
fit_func.SetParameter(0, h_mmumu.GetMaximum())  # Amplitude
fit_func.SetParameter(1, 91.2)                  # Mean (Z mass)
fit_func.SetParameter(2, 2.5)                   # Sigma
fit_func.SetParameter(3, 10)                    # Background constant
fit_func.SetParameter(4, -0.1)                  # Background slope
fit_func.SetParNames("Amplitude", "Mean", "Sigma", "BG const", "BG slope")
fit_func.SetLineColor(ROOT.kRed)
fit_func.SetLineWidth(2)

# Draw and fit
canvas = ROOT.TCanvas("canvas", "Z mass", 800, 600)
canvas.SetGrid()
h_mmumu.Draw("HIST")
h_mmumu.Fit(fit_func, "R")  # R = fit in defined range
fit_func.Draw("SAME")

# Add a legend with fit results
legend = ROOT.TLegend(0.6, 0.65, 0.88, 0.85)
legend.SetBorderSize(1)
legend.AddEntry(h_mmumu, "Data", "f")
legend.AddEntry(fit_func,
    f"Fit: #mu = {fit_func.GetParameter(1):.2f} GeV", "l")
legend.AddEntry(ROOT.nullptr,
    f"#sigma = {fit_func.GetParameter(2):.2f} GeV", "")
legend.AddEntry(ROOT.nullptr,
    f"#chi^{{2}}/NDF = {fit_func.GetChisquare():.1f}/{fit_func.GetNDF()}", "")
legend.Draw()

# PDG Z mass reference line
z_mass_line = ROOT.TLine(91.1876, 0, 91.1876, h_mmumu.GetMaximum())
z_mass_line.SetLineColor(ROOT.kGreen + 2)
z_mass_line.SetLineWidth(2)
z_mass_line.SetLineStyle(2)  # Dashed
z_mass_line.Draw()

canvas.Update()
canvas.SaveAs("zmass_fit.pdf")
print("Plot saved to zmass_fit.pdf")
```

---

## Getting Your Own Free API Key

The class proxy expires after the school. Here is how to get your own free access:

### Option 1: Google Gemini (Recommended)

Free tier: 15 requests per minute, 1 million tokens per day. No credit card required.

1. Go to **aistudio.google.com**
2. Sign in with your Google account (free to create)
3. Click **Get API key** then **Create API key**
4. Copy your key

Update `asp_assistant.py` — replace the `ask_assistant` function:

```python
GEMINI_API_KEY = "YOUR_KEY_HERE"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def ask_assistant(question):
    system_context = """You are a PyROOT plotting assistant for physics students.
    Generate complete, runnable PyROOT code with explanations."""

    payload = json.dumps({
        "contents": [{
            "parts": [{"text": system_context + "\n\nQuestion: " + question}]
        }]
    }).encode("utf-8")

    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    req = urllib.request.Request(
        url,
        data    = payload,
        headers = {"Content-Type": "application/json"},
        method  = "POST",
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["candidates"][0]["content"]["parts"][0]["text"]
```

### Option 2: OpenRouter (No Google account needed)

Free models available with any email address.

1. Go to **openrouter.ai**
2. Sign up with any email — no credit card needed
3. Go to **Keys** then **Create Key**
4. Use free models such as `meta-llama/llama-3.1-8b-instruct:free`

Update `asp_assistant.py`:

```python
OPENROUTER_API_KEY = "YOUR_KEY_HERE"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_assistant(question):
    payload = json.dumps({
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a PyROOT plotting assistant for physics students. Generate complete, runnable PyROOT code with explanations."
            },
            {"role": "user", "content": question}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_URL,
        data    = payload,
        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        method = "POST",
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"]
```

---

## Key Takeaways

- AI tools are coding collaborators, not autonomous scientists — they need good prompts and human verification
- The API pattern you used (HTTP POST with JSON, token authentication) is universal across all AI providers
- Distributed computing for AI training follows the same data-parallel patterns you used in HTCondor
- Free tiers exist for continued learning and experimentation after the school

---

## Further Reading

- Anthropic Claude API: <a href="https://platform.claude.com/docs/en/home" target="_blank">docs.anthropic.com</a>
- Google Gemini API: <a href="https://aistudio.google.com/prompts/new_chat" target="_blank">aistudio.google.com </a>
- OpenRouter free models: <a href="https://openrouter.ai/models?q=free" target="_blank">openrouter.ai/models?q=free</a>
- ROOT documentation: <a href="https://root.cern/doc/master/" target="_blank">root.cern/doc/master</a>
- HTCondor documentation: <a href="https://htcondor.org/htcondor/documentation/" target="_blank">htcondor.org/htcondor/documentation</a>
- WLCG: <a href="https://wlcg.web.cern.ch/" target="_blank">wlcg.web.cern.ch</a>

---

## Back to Exercises

[Materials Page](/dosar/ASP2026/ASP2026_Materials/)

---

*African School of Physics — Kenya 2026*
*Exercise designed by Julia Gray*
