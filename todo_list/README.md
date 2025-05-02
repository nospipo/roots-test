# Todo List Management Module

## การติดตั้ง

1. ย้ายโฟลเดอร์ todo_list ไปยังโฟลเดอร์ addons ของ Odoo:
   ```
   C:\Program Files (x86)\Odoo 16.0\server\odoo\addons\todo_list
   ```

2. รีสตาร์ท Odoo server

3. เปิด Odoo ในโหมด Developer:
   - เข้าไปที่ Odoo
   - กดปุ่ม Activate the developer mode (หรือกด Alt + D)
   - ไปที่ Apps > Update Apps List
   - ค้นหา "Todo List Management"
   - กด Install

## การใช้งาน

1. หลังจากติดตั้งเสร็จ จะเห็นเมนู "Todo Lists" ในเมนูหลัก
2. มี 3 เมนูย่อย:
   - All: แสดงรายการทั้งหมด
   - Uncomplete: แสดงรายการที่ยังไม่เสร็จ
   - Complete: แสดงรายการที่เสร็จแล้ว

## การสร้าง Todo List

1. กดปุ่ม Create
2. กรอกข้อมูลที่จำเป็น:
   - ชื่อ Todo List
   - วันที่เริ่มต้น
   - วันที่สิ้นสุด
   - Tags (มี Work, Event, Life เป็นค่าเริ่มต้น)
3. เพิ่มรายการย่อยได้โดยตรงในหน้า form
4. เพิ่มผู้เข้าร่วมได้ผ่าน field Participants

## การเปลี่ยนสถานะ

- Draft: สถานะเริ่มต้น
- In Progress: กดปุ่ม "Start Progress"
- Complete: กดปุ่ม "Done" เมื่อรายการย่อยทั้งหมดเสร็จแล้ว