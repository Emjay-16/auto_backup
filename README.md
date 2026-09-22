# Auto Backup System (Standalone & Mock Mode)

ระบบสำรองข้อมูลและกู้คืนข้อมูล (Auto Backup & Restore System) สำหรับ Robot (AMR / SMR / SMRL) และ Computer
โปรเจกต์นี้ได้รับการปรับปรุงให้ทำงานแบบ **Standalone Local & Mock Mode** บน Windows โดยไม่ต้องใช้ Docker หรือ PostgreSQL container 

---

## สรุปการตั้งค่าแบบ Mock Mode

- **Database**: ใช้ SQLite (`storage/auto_backup.db`) อัตโนมัติ พร้อม seed ข้อมูลจำลองเมื่อเริ่มระบบครั้งแรก
- **SFTP / SSH**: โหมดจำลอง (Mock) ไม่ต้องเชื่อมต่อ physical robot หรือ IP จริง
- **Robot MySQL**: โหมดจำลอง (Mock) ไม่ต้องต่อ MySQL server จริง
- **Frontend**: Next.js (Port 3000)
- **Backend API**: FastAPI (Port 8000)

---

## บัญชีผู้ใช้งานเริ่มต้น (Default Credentials)

| Username | Password | Role | สิทธิ์ |
|---|---|---|---|
| `admin` | `admin` | 1 | ผู้ดูแลระบบ (Admin) |
| `system` | `system` | 1 | ระบบ (System User) |

---

## วิธีเริ่มใช้งาน (Quick Start)

### วิธีที่ 1: รันพร้อมกันทั้งหมด (แนะนำ)
ดับเบิลคลิกไฟล์:
```
start_dev.bat
```
หรือรันผ่าน PowerShell:
```powershell
.\start_dev.ps1
```

### วิธีที่ 2: รันแยกตาม Service

**1. เริ่ม Backend API (FastAPI - Port 8000):**
ดับเบิลคลิก `start_api.bat` หรือรัน:
```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Health/Root: http://localhost:8000/
- API Swagger Docs: http://localhost:8000/docs

**2. เริ่ม Frontend Web (Next.js - Port 3000):**
ดับเบิลคลิก `start_web.bat` หรือรัน:
```powershell
cd front_end\my_app
npm run dev
```
- Web Application: http://localhost:3000

---

## ข้อมูลจำลองที่มีในระบบ (Mock Data)

1. **Device Groups**: `AMR`, `SMR`, `SMRL`, `Computer`
2. **Devices**:
   - `AMR 01` (172.30.39.101) - Online
   - `AMR 02` (172.30.39.102) - Offline
   - `AMR 03` (172.30.39.103) - Online
   - `AMR 04` (172.30.39.104) - Online
   - `SMR 02` (172.30.39.122) - Online
   - `SMR 03` (172.30.39.123) - Online
   - `API Server` (172.30.39.7) - Online
   - `Workstation Matrix` (172.30.39.10) - Online
3. **Backup Paths**: `/opt/robot/flows.json`, `/opt/robot/maps/`
4. **Mock Actions**:
   - กดปุ่ม **Backup** ระบบจะจำลองการดึงไฟล์และสร้างไฟล์เก็บไว้ที่ `storage/backups/` สำเร็จจริง
   - กดปุ่ม **Restore** ระบบจะบันทึก Log และรายงานผลสำเร็จจริง

