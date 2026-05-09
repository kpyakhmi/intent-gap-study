# Free Pilot via Google Colab

Run the Stage A filter on real WildChat data **for free, in your browser, with no installs**.

---

## What you need

- A Gmail / Google account. That's it.

## What you get

- Real funnel numbers from a 10,000-conversation WildChat sample (e.g., "X% of English ≥4-turn conversations contained a repair signal").
- 30 example matched conversations to eyeball.
- Two output files (`pilot_funnel.json`, `pilot_examples.jsonl`) you upload to the repo.

---

## Steps

1. Go to **https://colab.research.google.com**. Sign in with your Google account.
2. Click **File → Upload notebook** (top left menu).
3. Upload `code/colab_pilot.ipynb` from the GitHub repo, OR upload it directly from your local folder at `C:\Users\KP\Documents\Claude\Projects\Startup defensible moat\intent-gap-study\code\colab_pilot.ipynb`.
4. Once the notebook opens in Colab, click **Runtime → Run all** (top menu).
5. The first cell installs dependencies (~30 seconds). The data-streaming cell takes 2–4 minutes.
6. When all cells finish, look at the **Files panel on the left** of Colab (folder icon).
7. You'll see `pilot_funnel.json` and `pilot_examples.jsonl`. Right-click each → **Download**.
8. Open your GitHub repo in the browser. Go into the `data/` folder. Click **Add file → Upload files**. Drag in both downloaded files. Commit.

Done. You now have real preliminary numbers in the repo.

---

## Cost

$0. Colab's free tier is more than enough for this pilot.

## Privacy

WildChat is a public, AI2-licensed research dataset. Nothing private of yours touches the pilot. Colab runs on Google's servers and is sandboxed per your account.

## If anything errors

- **`load_dataset` fails on `allenai/WildChat-1M`**: WildChat-1M may require accepting AI2's license on Hugging Face. Visit https://huggingface.co/datasets/allenai/WildChat-1M, click "Agree and access," then re-run. You may also need to add a Hugging Face token to Colab — `huggingface-cli login` in a cell, paste a read token from https://huggingface.co/settings/tokens.
- **Out of memory**: drop `SAMPLE_SIZE` to 5,000 in cell 4.
- **Streaming is slow**: Colab's free tier sometimes throttles. Try again in 30 minutes or use a different time of day.

If you hit a wall, paste the error into Claude and we'll debug.
