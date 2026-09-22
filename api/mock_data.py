import logging
from datetime import datetime, timedelta
from decimal import Decimal
import bcrypt
from sqlalchemy.orm import Session

from api import constants, models
from api.utils.time import now_local

logger = logging.getLogger(__name__)


def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def seed_mock_data(db: Session) -> None:
    """Seed initial mock data for local standalone / mock development."""
    now = now_local()

    # 1. Users
    admin_user = db.query(models.User).filter(models.User.user_name == "admin").first()
    if not admin_user:
        admin_user = models.User(
            user_name="admin",
            password=hash_pw("admin"),
            role=constants.ROLE_ADMIN,
        )
        db.add(admin_user)

    system_user = db.query(models.User).filter(models.User.user_name == "system").first()
    if not system_user:
        system_user = models.User(
            user_name="system",
            password="system",  # Plain text or hash is accepted by auth.py
            role=constants.ROLE_ADMIN,
        )
        db.add(system_user)

    db.flush()

    # 2. Device Groups
    group_names = ["AMR", "SMR", "SMRL", "Computer"]
    groups = {}
    for name in group_names:
        g = db.query(models.DeviceGroup).filter(models.DeviceGroup.group_name == name).first()
        if not g:
            g = models.DeviceGroup(group_name=name)
            db.add(g)
            db.flush()
        groups[name] = g

    # 3. Devices
    mock_devices = [
        {
            "group": "AMR",
            "device_code": "4PS00901",
            "device_name": "AMR 01",
            "ip_address": "172.30.39.101",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": True,
        },
        {
            "group": "AMR",
            "device_code": "4PS00902",
            "device_name": "AMR 02",
            "ip_address": "172.30.39.102",
            "status": constants.DEVICE_STATUS_OFFLINE,
            "auto_backup": False,
        },
        {
            "group": "AMR",
            "device_code": "4PS00903",
            "device_name": "AMR 03",
            "ip_address": "172.30.39.103",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": True,
        },
        {
            "group": "AMR",
            "device_code": "4B000404",
            "device_name": "AMR 04",
            "ip_address": "172.30.39.104",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": True,
        },
        {
            "group": "SMR",
            "device_code": "0002APM044",
            "device_name": "SMR 02",
            "ip_address": "172.30.39.122",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": True,
        },
        {
            "group": "SMR",
            "device_code": "0003APM044",
            "device_name": "SMR 03",
            "ip_address": "172.30.39.123",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": True,
        },
        {
            "group": "Computer",
            "device_code": "COMP-SERVER-01",
            "device_name": "API Server",
            "ip_address": "172.30.39.7",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": False,
        },
        {
            "group": "Computer",
            "device_code": "COMP-WORKSTATION-01",
            "device_name": "Workstation Matrix",
            "ip_address": "172.30.39.10",
            "status": constants.DEVICE_STATUS_ONLINE,
            "auto_backup": True,
        },
    ]

    saved_devices = {}
    for d in mock_devices:
        existing = db.query(models.Device).filter(models.Device.ip_address == d["ip_address"]).first()
        if not existing:
            existing = models.Device(
                group_id=groups[d["group"]].group_id,
                device_code=d["device_code"],
                device_name=d["device_name"],
                ip_address=d["ip_address"],
                device_status=d["status"],
                auto_backup_enabled=d["auto_backup"],
                last_seen_at=now if d["status"] == constants.DEVICE_STATUS_ONLINE else None,
                created_at=now - timedelta(days=30),
                updated_at=now,
            )
            db.add(existing)
            db.flush()
        saved_devices[d["device_code"]] = existing

    # 4. Device Backup Paths
    default_paths = [
        ("/opt/robot/flows.json", "Node-RED flows"),
        ("/opt/robot/maps/", "Maps Directory"),
    ]
    for dev in saved_devices.values():
        for path, label in default_paths:
            existing_path = (
                db.query(models.DeviceBackupPath)
                .filter(
                    models.DeviceBackupPath.device_id == dev.device_id,
                    models.DeviceBackupPath.path == path,
                )
                .first()
            )
            if not existing_path:
                db.add(
                    models.DeviceBackupPath(
                        device_id=dev.device_id,
                        path=path,
                        label=label,
                        created_at=now - timedelta(days=20),
                    )
                )

    db.flush()

    # 5. Sample Backups
    existing_backups_count = db.query(models.Backup).count()
    if existing_backups_count == 0:
        dev1 = saved_devices.get("4PS00901")
        dev3 = saved_devices.get("4PS00903")
        dev5 = saved_devices.get("0002APM044")

        sample_backups = [
            {
                "device": dev1,
                "name": f"AUTO_{dev1.device_code}_{(now - timedelta(days=1)).strftime('%Y%m%d_%H%M%S')}",
                "type": constants.BACKUP_TYPE_AUTO,
                "status": constants.BACKUP_STATUS_SUCCESS,
                "files": 4,
                "size": Decimal("12.45"),
                "time": now - timedelta(days=1),
            },
            {
                "device": dev3,
                "name": f"AUTO_{dev3.device_code}_{(now - timedelta(days=2)).strftime('%Y%m%d_%H%M%S')}",
                "type": constants.BACKUP_TYPE_AUTO,
                "status": constants.BACKUP_STATUS_SUCCESS,
                "files": 3,
                "size": Decimal("8.20"),
                "time": now - timedelta(days=2),
            },
            {
                "device": dev5,
                "name": f"MANUAL_{dev5.device_code}_{(now - timedelta(hours=5)).strftime('%Y%m%d_%H%M%S')}",
                "type": constants.BACKUP_TYPE_SELECTED,
                "status": constants.BACKUP_STATUS_SUCCESS,
                "files": 2,
                "size": Decimal("5.10"),
                "time": now - timedelta(hours=5),
            },
        ]

        for b in sample_backups:
            if not b["device"]:
                continue
            backup = models.Backup(
                device_id=b["device"].device_id,
                backup_name=b["name"],
                backup_type=b["type"],
                backup_status=b["status"],
                total_file=b["files"],
                total_size_mb=b["size"],
                created_by=admin_user.user_id,
                created_at=b["time"],
                updated_at=b["time"],
            )
            db.add(backup)
            db.flush()

            # Backup Files
            f1 = models.BackupFile(
                backup_id=backup.backup_id,
                file_name="flows.json",
                file_path=f"storage/backups/{b['device'].device_code}/flows.json",
                file_type="json",
                file_size_mb=Decimal("1.25"),
                checksum="mock-checksum-flows-sha256",
                file_status=1,
                created_at=b["time"],
            )
            f2 = models.BackupFile(
                backup_id=backup.backup_id,
                file_name="map.yaml",
                file_path=f"storage/backups/{b['device'].device_code}/map.yaml",
                file_type="yaml",
                file_size_mb=Decimal("3.85"),
                checksum="mock-checksum-map-sha256",
                file_status=1,
                created_at=b["time"],
            )
            db.add_all([f1, f2])

            # Activity Log
            db.add(
                models.ActivityLog(
                    user_id=admin_user.user_id,
                    device_id=b["device"].device_id,
                    backup_id=backup.backup_id,
                    action="BACKUP",
                    activity_status=constants.BACKUP_STATUS_SUCCESS,
                    activity_message=f"Backup {backup.backup_name} completed successfully (Mock)",
                    created_at=b["time"],
                )
            )

    # 6. Sample Jobs
    existing_jobs_count = db.query(models.BackupJob).count()
    if existing_jobs_count == 0:
        dev1 = saved_devices.get("4PS00901")
        if dev1:
            job = models.BackupJob(
                job_type="AUTO_BACKUP",
                job_status=constants.JOB_STATUS_SUCCESS,
                device_id=dev1.device_id,
                requested_by=system_user.user_id,
                total_devices=1,
                checked_devices=1,
                online_devices=1,
                offline_devices=0,
                backups_created=1,
                failed_devices=0,
                job_message="Auto backup completed successfully (Mock)",
                started_at=now - timedelta(days=1),
                finished_at=now - timedelta(days=1) + timedelta(minutes=2),
                updated_at=now - timedelta(days=1) + timedelta(minutes=2),
            )
            db.add(job)

    db.commit()
    logger.info("Mock data successfully seeded.")

