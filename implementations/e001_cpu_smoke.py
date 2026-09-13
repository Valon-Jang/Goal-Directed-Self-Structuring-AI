"""E0.1: bounded REAL MODEL developmental smoke, NOT BARE/HUMAN comparison.

Run from repo root: python -m implementations.e001_cpu_smoke --execute
Only public pinned assets are downloaded. Model receives the existing closed
E001 action interface, no shell, filesystem, credentials, reference solver or
answer keys. A new server process per task resets model state; CPU limits,
per-request alarm, per-case watchdog and workflow timeout bound this instrument.
No claims about hosted API billing caps or malicious-host OS isolation are made.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import signal
import socket
import subprocess
import tarfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from .e001_measurement import Ledger, canonical, sha, extract_action

MODEL_REVISION = '23749fefcc72300e3a2ad315e1317431b06b590a'
MODEL_SHA = '9465e63a22add5354d9bb4b99e90117043c7124007664907259bd16d043bb031'
RUNTIME_SHA = '01b90b0764821d0e53b985730eea3837e29a976ee00e783e18837937b93fc3f1'
MODEL_URL = f'https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/resolve/{MODEL_REVISION}/Qwen3-0.6B-Q8_0.gguf'
RUNTIME_URL = 'https://github.com/ggml-org/llama.cpp/releases/download/b10344/llama-b10344-bin-ubuntu-x64.tar.gz'
SETTINGS = {'temperature': .7, 'top_p': .8, 'top_k': 20, 'min_p': 0.,
            'presence_penalty': 1.5, 'max_tokens': 768, 'seed': 913,
            'cache_prompt': False, 'response_format': {'type': 'json_object'},
            'chat_template_kwargs': {'enable_thinking': False}, 'stream': False}
MANIFEST = {'experiment': 'E001-E01-CPU-SMOKE-v1',
            'evidence_class': 'REAL_MODEL_DEVELOPMENTAL_SINGLE_ARM',
            'model': 'Qwen/Qwen3-0.6B-GGUF:Q8_0', 'model_revision': MODEL_REVISION,
            'model_sha256': MODEL_SHA, 'runtime': 'llama.cpp-b10344',
            'runtime_archive_sha256': RUNTIME_SHA, 'settings': SETTINGS,
            'arm': 'BARE-GOAL', 'families': ['state', 'quality', 'approval'],
            'variant': 0, 'max_calls_per_task': 6, 'one_format_repair': True,
            'request_seconds': 60, 'server_lifetime_seconds': 180,
            'workflow_command_seconds': 660, 'model_context_tokens': 8192,
            'permissions': 'closed-read-only-synthetic-E001-tools',
            'human_fact_source': 'SCRIPTED_SYNTHETIC_NOT_A_PARTICIPANT'}


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def acquire(url: str, target: Path, expected_sha: str, max_bytes: int) -> dict:
    # One request, bounded transfer, no credentials; no auth bypass or silent retry.
    completed = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
        '--connect-timeout', '20', '--max-time', '180', '--max-filesize', str(max_bytes),
        '--output', str(target), url], capture_output=True, timeout=190)
    if completed.returncode:
        # Do not print signed redirects or complete URLs embedded in HTTP errors.
        raise RuntimeError(f'PUBLIC_DOWNLOAD_FAILED_CURL_{completed.returncode}')
    actual = file_sha(target)
    if actual != expected_sha:
        raise RuntimeError('ASSET_SHA256_MISMATCH')
    return {'sha256': actual, 'bytes': target.stat().st_size, 'verified': True}


class OwnedServer:
    def __init__(self, binary: Path, model: Path, folder: Path):
        self.folder, self.process, self.watchdog = folder, None, None
        self.deadline_hit = threading.Event()
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            self.port = s.getsockname()[1]
        self.base = f'http://127.0.0.1:{self.port}'
        self.command = [str(binary), '-m', str(model), '-c', '8192', '-np', '1',
            '-t', '2', '-ngl', '0', '--host', '127.0.0.1', '--port', str(self.port),
            '--alias', MODEL_SHA, '--offline', '--no-agent', '--no-webui',
            '--no-cache-prompt', '--jinja', '--reasoning', 'off',
            '--chat-template-kwargs', '{"enable_thinking":false}', '--log-verbosity', '1']
        libdirs = sorted({str(p.parent) for p in binary.parent.parent.rglob('*.so*')})
        self.env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
                    'HOME': str(folder), 'LANG': 'C.UTF-8', 'LD_LIBRARY_PATH': ':'.join(libdirs)}

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.process.wait(timeout=5)

    def __enter__(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        self.log = (self.folder / 'server.log').open('wb')
        self.process = subprocess.Popen(self.command, env=self.env, stdout=self.log,
                                        stderr=subprocess.STDOUT, start_new_session=True)
        def expired():
            self.deadline_hit.set()
            self.stop()
        self.watchdog = threading.Timer(MANIFEST['server_lifetime_seconds'], expired)
        self.watchdog.daemon = True
        self.watchdog.start()
        try:
            for _ in range(90):
                if self.process.poll() is not None:
                    raise RuntimeError('SERVER_EXITED_BEFORE_HEALTH')
                try:
                    with urllib.request.urlopen(self.base + '/health', timeout=1) as r:
                        if r.status == 200:
                            return self
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(.5)
            raise TimeoutError('SERVER_START_TIMEOUT')
        except Exception:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *args):
        if self.watchdog:
            self.watchdog.cancel()
        self.stop()
        self.log.close()

    def request(self, messages: list[dict], max_tokens: int = 768) -> dict:
        body = {**SETTINGS, 'max_tokens': min(max_tokens, SETTINGS['max_tokens']),
                'model': MODEL_SHA, 'messages': messages}
        request = urllib.request.Request(self.base + '/v1/chat/completions',
                   data=canonical(body).encode(), headers={'Content-Type': 'application/json'})
        old = signal.getsignal(signal.SIGALRM)
        def timeout(_signum, _frame):
            self.stop()
            raise TimeoutError('LOCAL_INFERENCE_DEADLINE')
        signal.signal(signal.SIGALRM, timeout)
        signal.setitimer(signal.ITIMER_REAL, MANIFEST['request_seconds'])
        try:
            with urllib.request.urlopen(request, timeout=MANIFEST['request_seconds']) as r:
                return json.load(r)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)


def execute_case(binary, model, folder, family, ledger):
    from benchmarks.e001_tasks import make_task
    from .e001_harness import Environment, INTERFACE, TOOLS
    task = make_task(family)
    facts = lambda key, q: {'value': task.human_facts[key], 'active_seconds': None,
                            'source': 'SCRIPTED_SYNTHETIC_NOT_A_PARTICIPANT'}
    env = Environment(task, facts, max_actions=6)
    initial = {'interface': INTERFACE, **env.public()}
    messages = [{'role': 'system', 'content': INTERFACE},
                {'role': 'user', 'content': canonical(initial)}]
    calls, parse_errors, usage, errors = 0, 0, [], []
    valid_actions = 0
    started = time.monotonic()
    try:
        with OwnedServer(binary, model, folder / family) as server:
            for index in range(MANIFEST['max_calls_per_task']):
                call_id = f'{family}/{index}'
                ledger.begin(call_id, sha(messages))
                calls += 1
                try:
                    response = server.request(messages)
                    use = response.get('usage')
                    usage.append(use)
                    choice = response['choices'][0]
                    text = choice['message'].get('content') or ''
                    # Only visible output fingerprint and actions are retained.
                    ledger.end(call_id, 'COMPLETED', usage=use,
                        visible_output_sha256=hashlib.sha256(text.encode()).hexdigest(),
                        finish_reason=choice.get('finish_reason'),
                        provider_model=response.get('model'))
                except Exception as exc:
                    code = type(exc).__name__
                    ledger.end(call_id, 'TIMEOUT' if isinstance(exc, TimeoutError) else 'FAILED', error=code)
                    errors.append(code)
                    break
                try:
                    action = extract_action(text, set(TOOLS))
                except ValueError as exc:
                    parse_errors += 1
                    ledger.append('FORMAT_REJECTED', task=family, error=str(exc))
                    if parse_errors > 1:
                        errors.append('FORMAT_REPAIR_EXHAUSTED')
                        break
                    # Interface-only recovery. No suggested SQL, method or answer.
                    messages.append({'role': 'user', 'content': 'No action executed. Return exactly one JSON object with tool and args from the interface.'})
                    continue
                valid_actions += 1
                tool_result = env.step(action)
                ledger.append('TOOL_RESULT', task=family, action=action, response=tool_result)
                messages.extend([{'role': 'assistant', 'content': canonical(action)},
                                 {'role': 'user', 'content': canonical(tool_result)}])
                if env.submitted or env.budget_exhausted:
                    break
        if not env.submitted and calls >= MANIFEST['max_calls_per_task']:
            env.budget_exhausted = True
        outcome = env.outcome()
        if errors:
            outcome['accepted'] = False
        result = {'task_id': task.task_id, 'family': family, 'arm': 'BARE-GOAL',
                  'model_calls_attempted': calls, 'valid_model_actions': valid_actions,
                  'format_errors': parse_errors, 'usage': usage, 'errors': errors,
                  'outcome': outcome, 'trace': env.trace, 'capsules_created': len(env.capsules),
                  'wall_seconds': time.monotonic()-started, 'initial_sha256': sha(initial)}
        ledger.append('EPISODE_COMPLETED', result=result)
        return result
    finally:
        env.close()


def run(folder: Path) -> dict:
    report = {'manifest': MANIFEST, 'manifest_sha256': sha(MANIFEST),
              'status': 'STARTED', 'stage': 'INITIALIZE', 'commit': os.environ.get('GITHUB_SHA'),
              'workflow_run_id': os.environ.get('GITHUB_RUN_ID'), 'python': platform.python_version(),
              'real_model_calls_attempted': 0, 'primary_trials_completed': 0,
              'human_guides_observed': 0, 'human_total_active_seconds': None,
              'hosted_model_api_spend_usd': 0, 'total_compute_cost_usd': None, 'cases': []}
    folder.mkdir(parents=True, exist_ok=False)
    ledger = Ledger(folder / 'trace.jsonl', sha(MANIFEST))
    try:
        report['stage'] = 'RUNTIME_ACQUISITION'
        archive = folder / 'runtime.tar.gz'
        report['runtime_asset'] = acquire(RUNTIME_URL, archive, RUNTIME_SHA, 50000000)
        runtime_dir = folder / 'runtime'
        runtime_dir.mkdir()
        with tarfile.open(archive, 'r:gz') as tar:
            tar.extractall(runtime_dir, filter='data')
        candidates = list(runtime_dir.rglob('llama-server'))
        if len(candidates) != 1:
            raise RuntimeError('UNEXPECTED_RUNTIME_LAYOUT')
        binary = candidates[0]
        binary.chmod(0o755)
        report['binary_sha256'] = file_sha(binary)
        report['stage'] = 'MODEL_ACQUISITION'
        model = folder / 'model.gguf'
        report['model_asset'] = acquire(MODEL_URL, model, MODEL_SHA, 800000000)
        report['stage'] = 'MODEL_TOOL_EPISODES'
        for family in MANIFEST['families']:
            case = execute_case(binary, model, folder, family, ledger)
            report['cases'].append(case)
            report['real_model_calls_attempted'] += case['model_calls_attempted']
            (folder / 'partial.json').write_text(canonical(report), encoding='utf-8')
            print('E01_CASE ' + canonical({k: case[k] for k in ('family', 'model_calls_attempted', 'valid_model_actions', 'format_errors', 'errors')}), flush=True)
        report['status'] = 'COMPLETED_EXPLORATORY'
        report['stage'] = 'DONE'
    except Exception as exc:
        report['status'] = 'EXECUTION_BLOCKED'
        report['error_class'] = type(exc).__name__
        # These errors are normalized by our code; do not expose request URLs/tokens.
        report['error_code'] = str(exc)[:180] if isinstance(exc, (RuntimeError, TimeoutError)) else type(exc).__name__
    finally:
        report['real_model_calls_attempted'] = sum(r['event'] == 'CALL_STARTED' for r in ledger.rows)
        report['real_model_responses_completed'] = sum(r['event'] == 'CALL_COMPLETED' for r in ledger.rows)
        report['unresolved_calls'] = ledger.unresolved()
        report['ledger_sha256'] = file_sha(folder / 'trace.jsonl') if (folder / 'trace.jsonl').exists() else None
        report['source_sha256'] = {p: file_sha(Path(p)) for p in [
            'implementations/e001_cpu_smoke.py', 'implementations/e001_measurement.py',
            'implementations/e001_harness.py', 'benchmarks/e001_tasks.py']}
        report['claim_boundary'] = 'Small public developmental single-arm smoke. No human-method comparison, efficacy superiority, held-out generalization or measured human labor.'
        (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print('E01_REPORT_BEGIN\n' + json.dumps(report, ensure_ascii=False, indent=2) + '\nE01_REPORT_END', flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', required=True)
    parser.add_argument('--out', default='e01-output')
    args = parser.parse_args()
    result = run(Path(args.out).resolve())
    raise SystemExit(0 if result['status'] == 'COMPLETED_EXPLORATORY' else 2)
