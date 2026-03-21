# KernelFinance Pro

KernelFinance Pro now has one supported desktop app:

- `Python desktop app`
  - Main file: `kernel_finance_pro.py`
  - Uses Tkinter
  - Canonical launcher: `./run_app.sh`

The older Node.js/Electron version in `js-frontend/` is kept only as legacy source and is no longer the recommended app path.

## Run The App

```bash
./run_app.sh
```

## Notes

- `./run_python_app.sh` still works and forwards to `./run_app.sh`.
- `./run_node_app.sh` is now a compatibility shim that launches the Python app.
- The Python app is the single supported product going forward.
- Logo assets are shared from `assets/logo.png`.
