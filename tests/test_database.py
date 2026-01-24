"""
데이터베이스 모델 테스트
"""
import os
import sys
import pytest
from datetime import datetime, date
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDatabaseSetup:
    """데이터베이스 설정 테스트"""

    def test_schema_name_defined(self):
        """스키마 이름 정의 확인"""
        from database_setup import SCHEMA_NAME
        assert SCHEMA_NAME == "qhyx_growth"

    def test_kst_timezone(self):
        """한국 시간대 설정 확인"""
        from database_setup import KST, get_kst_now
        from datetime import timezone, timedelta

        assert KST == timezone(timedelta(hours=9))
        now = get_kst_now()
        assert isinstance(now, datetime)


class TestActivityLogModel:
    """ActivityLog 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import ActivityLog

        assert hasattr(ActivityLog, 'id')
        assert hasattr(ActivityLog, 'timestamp')
        assert hasattr(ActivityLog, 'activity_type')
        assert hasattr(ActivityLog, 'description')
        assert hasattr(ActivityLog, 'status')

    def test_table_name(self):
        """테이블 이름 확인"""
        from database_setup import ActivityLog
        assert ActivityLog.__tablename__ == 'activity_logs'


class TestSyncLogModel:
    """SyncLog 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import SyncLog

        assert hasattr(SyncLog, 'id')
        assert hasattr(SyncLog, 'timestamp')
        assert hasattr(SyncLog, 'action')
        assert hasattr(SyncLog, 'message')
        assert hasattr(SyncLog, 'status')
        assert hasattr(SyncLog, 'duration_ms')


class TestEmployeeModel:
    """Employee 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import Employee

        assert hasattr(Employee, 'id')
        assert hasattr(Employee, 'employee_id')
        assert hasattr(Employee, 'name')
        assert hasattr(Employee, 'role')
        assert hasattr(Employee, 'department')
        assert hasattr(Employee, 'status')

    def test_employee_relationships(self):
        """관계 필드 확인"""
        from database_setup import Employee

        assert hasattr(Employee, 'tasks')
        assert hasattr(Employee, 'suggestions')


class TestTaskModel:
    """Task 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import Task

        assert hasattr(Task, 'id')
        assert hasattr(Task, 'task_id')
        assert hasattr(Task, 'title')
        assert hasattr(Task, 'status')
        assert hasattr(Task, 'priority')
        assert hasattr(Task, 'assigned_to')

    def test_task_relationship(self):
        """Employee 관계 확인"""
        from database_setup import Task
        assert hasattr(Task, 'employee')


class TestBusinessMeetingModel:
    """BusinessMeeting 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import BusinessMeeting

        assert hasattr(BusinessMeeting, 'id')
        assert hasattr(BusinessMeeting, 'meeting_type')
        assert hasattr(BusinessMeeting, 'title')
        assert hasattr(BusinessMeeting, 'agenda')
        assert hasattr(BusinessMeeting, 'participants')
        assert hasattr(BusinessMeeting, 'key_decisions')
        assert hasattr(BusinessMeeting, 'meeting_date')


class TestBusinessPlanModel:
    """BusinessPlan 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import BusinessPlan

        assert hasattr(BusinessPlan, 'id')
        assert hasattr(BusinessPlan, 'plan_name')
        assert hasattr(BusinessPlan, 'plan_type')
        assert hasattr(BusinessPlan, 'target_market')
        assert hasattr(BusinessPlan, 'revenue_model')
        assert hasattr(BusinessPlan, 'projected_revenue_12m')
        assert hasattr(BusinessPlan, 'risk_level')
        assert hasattr(BusinessPlan, 'feasibility_score')


class TestEmployeeSuggestionModel:
    """EmployeeSuggestion 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import EmployeeSuggestion

        assert hasattr(EmployeeSuggestion, 'id')
        assert hasattr(EmployeeSuggestion, 'suggestion_id')
        assert hasattr(EmployeeSuggestion, 'employee_id')
        assert hasattr(EmployeeSuggestion, 'category')
        assert hasattr(EmployeeSuggestion, 'title')
        assert hasattr(EmployeeSuggestion, 'description')
        assert hasattr(EmployeeSuggestion, 'status')

    def test_suggestion_relationship(self):
        """Employee 관계 확인"""
        from database_setup import EmployeeSuggestion
        assert hasattr(EmployeeSuggestion, 'employee')


class TestCompanyMetricModel:
    """CompanyMetric 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import CompanyMetric

        assert hasattr(CompanyMetric, 'id')
        assert hasattr(CompanyMetric, 'date')
        assert hasattr(CompanyMetric, 'metric_name')
        assert hasattr(CompanyMetric, 'value')
        assert hasattr(CompanyMetric, 'category')


class TestRevenueModel:
    """Revenue 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import Revenue

        assert hasattr(Revenue, 'id')
        assert hasattr(Revenue, 'date')
        assert hasattr(Revenue, 'source')
        assert hasattr(Revenue, 'amount')
        assert hasattr(Revenue, 'currency')
        assert hasattr(Revenue, 'category')


class TestSystemHealthModel:
    """SystemHealth 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import SystemHealth

        assert hasattr(SystemHealth, 'id')
        assert hasattr(SystemHealth, 'timestamp')
        assert hasattr(SystemHealth, 'service_name')
        assert hasattr(SystemHealth, 'status')
        assert hasattr(SystemHealth, 'response_time_ms')
        assert hasattr(SystemHealth, 'cpu_usage')
        assert hasattr(SystemHealth, 'memory_usage')


class TestGitCommitModel:
    """GitCommit 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import GitCommit

        assert hasattr(GitCommit, 'id')
        assert hasattr(GitCommit, 'commit_hash')
        assert hasattr(GitCommit, 'author')
        assert hasattr(GitCommit, 'message')
        assert hasattr(GitCommit, 'timestamp')
        assert hasattr(GitCommit, 'branch')


class TestStartupSupportProgramModel:
    """StartupSupportProgram 모델 테스트"""

    def test_model_has_required_fields(self):
        """필수 필드 존재 확인"""
        from database_setup import StartupSupportProgram

        assert hasattr(StartupSupportProgram, 'id')
        assert hasattr(StartupSupportProgram, 'program_id')
        assert hasattr(StartupSupportProgram, 'name')
        assert hasattr(StartupSupportProgram, 'organization')
        assert hasattr(StartupSupportProgram, 'category')


class TestAllModelsHaveSchema:
    """모든 모델이 스키마 설정 확인"""

    def test_all_models_use_correct_schema(self):
        """모든 모델이 qhyx_growth 스키마 사용"""
        from database_setup import (
            ActivityLog, SyncLog, CompanyMetric, GitCommit,
            Employee, Task, SystemHealth, CompanyMilestone,
            Revenue, BusinessMeeting, BusinessPlan, EmployeeSuggestion,
            SCHEMA_NAME
        )

        models = [
            ActivityLog, SyncLog, CompanyMetric, GitCommit,
            Employee, Task, SystemHealth, CompanyMilestone,
            Revenue, BusinessMeeting, BusinessPlan, EmployeeSuggestion
        ]

        for model in models:
            # __table_args__가 dict이거나 tuple일 수 있음
            table_args = model.__table_args__
            if isinstance(table_args, dict):
                assert table_args.get('schema') == SCHEMA_NAME, \
                    f"{model.__name__} doesn't use correct schema"
            elif isinstance(table_args, tuple):
                # 마지막 요소가 dict인 경우
                for arg in table_args:
                    if isinstance(arg, dict) and 'schema' in arg:
                        assert arg['schema'] == SCHEMA_NAME, \
                            f"{model.__name__} doesn't use correct schema"
                        break
