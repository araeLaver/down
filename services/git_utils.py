import subprocess
from datetime import datetime
import git

try:
    repo = git.Repo('.')
except:
    repo = None


def parse_sync_log():
    """sync.log 파일 파싱하여 데이터베이스에 저장"""
    from database_setup import SyncLog
    from services.db import Session

    session = Session()
    try:
        with open('sync.log', 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.strip():
                try:
                    parts = line.split(']', 2)
                    if len(parts) >= 3:
                        timestamp_str = parts[0].strip('[')
                        log_type = parts[1].strip(' [')
                        message = parts[2].strip()

                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                        existing = session.query(SyncLog).filter_by(
                            timestamp=timestamp,
                            action=log_type,
                            message=message
                        ).first()

                        if not existing:
                            sync_log = SyncLog(
                                timestamp=timestamp,
                                action=log_type,
                                message=message,
                                status='success' if 'ERROR' not in message.upper() else 'error'
                            )
                            session.add(sync_log)
                except Exception as e:
                    print(f"Error parsing line: {e}")

        session.commit()
    except FileNotFoundError:
        pass
    finally:
        session.close()


def get_git_stats():
    """Git 저장소 통계"""
    if not repo:
        return {}

    try:
        return {
            'current_branch': repo.active_branch.name,
            'total_commits': len(list(repo.iter_commits())),
            'uncommitted_changes': len(repo.index.diff(None)) + len(repo.untracked_files),
            'last_commit': {
                'hash': repo.head.commit.hexsha[:7],
                'message': repo.head.commit.message.strip(),
                'author': str(repo.head.commit.author),
                'date': datetime.fromtimestamp(repo.head.commit.committed_date).isoformat()
            }
        }
    except:
        return {}


def get_sync_status():
    """동기화 데몬 상태 확인"""
    try:
        result = subprocess.run(['./sync-control.sh', 'status'],
                              capture_output=True, text=True)
        is_running = 'PID:' in result.stdout

        if is_running:
            pid_start = result.stdout.find('PID:') + 4
            pid_end = result.stdout.find(')', pid_start)
            pid = result.stdout[pid_start:pid_end].strip()
            return {'running': True, 'pid': pid}
        else:
            return {'running': False, 'pid': None}
    except:
        return {'running': False, 'pid': None}
