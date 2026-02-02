# -*- coding: utf-8 -*-
"""HWP 사업계획서 양식에 내용 채우기 - Mini-stream 기반 OLE 수정"""
import olefile, zlib, struct, shutil, math

SRC = 'docs/[플랫폼]+사업계획서(컨설팅+신청시+필수제출).hwp'
DST = 'docs/사업계획서_작성완료.hwp'

SECTOR_SIZE = 512
MINI_SECTOR_SIZE = 64

# === 1. Read & decompress ===
ole = olefile.OleFileIO(SRC)
body_compressed = ole.openstream('BodyText/Section0').read()
body = zlib.decompress(body_compressed, -15)
ole.close()

# === 2. Parse HWP tagged records ===
records = []
i = 0; idx = 0
while i < len(body):
    if i + 4 > len(body): break
    hdr_val = struct.unpack('<I', body[i:i+4])[0]
    tag = hdr_val & 0x3FF
    lvl = (hdr_val >> 10) & 0x3FF
    sz = (hdr_val >> 20) & 0xFFF
    hdr_bytes = body[i:i+4]
    if sz == 0xFFF:
        if i + 8 > len(body): break
        sz = struct.unpack('<I', body[i+4:i+8])[0]
        hdr_bytes = body[i:i+8]
        i += 8
    else:
        i += 4
    records.append({'i': idx, 'tag': tag, 'lvl': lvl, 'sz': sz, 'hdr': hdr_bytes, 'raw': body[i:i+sz]})
    i += sz; idx += 1

# === 3. Content to fill ===
content_map = {}
history = [
    ("2025. 8", "TravelMate 사업 아이디어 구상 및 시장 조사 착수"),
    ("2025. 10", "AI 기반 동행 매칭 알고리즘 프로토타입 개발"),
    ("2025. 12", "블록체인(Polygon) NFT 발행 시스템 기술 검증 완료"),
    ("2026. 1", "경기스타트업플랫폼 예비창업 전문가지원 사업계획서 제출"),
]
for row, (date, desc) in enumerate(history):
    content_map[54 + row * 8] = date
    content_map[58 + row * 8] = desc

content_map[105] = "TravelMate - AI 여행 동행 매칭 및 위치 인증 NFT 수집 플랫폼"
content_map[114] = (
    "TravelMate는 AI 기반 여행 동행 매칭과 블록체인 위치 인증 NFT 수집을 결합한 모바일 플랫폼입니다. "
    "국내 1인 여행자 수는 매년 15% 이상 증가하고 있으나, 혼자 여행하는 MZ세대가 현지에서 동행자를 찾기 어렵고, "
    "여행 추억을 체계적으로 기록할 수단이 부재합니다. "
    "TravelMate는 AI가 취향/일정/위치를 분석하여 최적의 동행자를 실시간 추천하고, "
    "GPS 위치 인증을 통해 방문한 관광지를 Polygon NFT로 자동 발행합니다. "
    "2026년 MVP 출시 후 1년 내 MAU 5만 명, NFT 10만 건 달성이 목표입니다."
)
content_map[123] = (
    "1) AI 동행 매칭: 관심사/스타일/일정/위치 종합 분석, 실시간 추천. "
    "2) GPS 위치 인증 NFT: 관광지 방문 시 GPS 인증으로 NFT 자동 발행(Polygon ERC-721, 가스비 1~5원). "
    "3) NFT 마켓플레이스: 수집 NFT 거래(수수료 3~5%), 경매 기능. "
    "4) B2B 지자체 연계: 지역 한정 NFT 발행, 보유자 현지 혜택. "
    "기술: Spring Boot, React Native, Polygon, Python AI/ML, AWS."
)
content_map[132] = (
    "TAM 글로벌 여행산업 1,560조원. SAM 아시아 1인여행 65조원. SOM 한국 MZ세대 6,500억원. "
    "1인 여행자 비율 2023년 27%에서 2025년 35%로 증가. MZ '혼행' 검색량 연 40%+ 증가. "
    "경쟁사: 여행에미치다(AI매칭없음), TripFriend(외국인대상). "
    "동행매칭+NFT 결합 서비스 국내외 전무, 선점 효과 극대화 가능."
)
content_map[145] = (
    "자금: 전문가지원 1억+자기자본 2천만+시드 3~5억. "
    "12개월 사용: 인건비 4,800만(40%), 서버 1,200만(10%), 블록체인 600만(5%), "
    "마케팅 2,400만(20%), 디자인 1,200만(10%), 법무 600만(5%), 기타 1,200만(10%). "
    "마일스톤: 1~3월 MVP, 4~5월 베타(500명), 6월 출시, 7~9월 마켓+구독, 10~12월 B2B+투자. "
    "수익: NFT수수료 5억, 구독 3억, B2B 2억, 광고 1억. 3년차 50억."
)
content_map[167] = (
    "1) 블록체인/AI 전문 개발 인력 확보 시급(현재 대표 1인 개발). "
    "2) 동행 매칭 네트워크 효과를 위한 초기 고객 확보 전략 필요. "
    "3) NFT 거래 세금, GPS 개인정보, 특금법 등 규제 대응 법률 자문 필수. "
    "4) 지자체/관광공사 B2B 파트너십 구축 시 공공기관 접근 어려움."
)
content_map[176] = (
    "사업: 국내 최초 AI동행+NFT 플랫폼 선점. 1년 MAU 5만, 3년 매출 50억, 고용 20명. "
    "기술: GPS NFT 특허, AI 매칭 90%+, Polygon 초저비용 실증. "
    "사회: 안전 동행 문화, 비수도권 관광 활성화, 블록체인 대중화. "
    "지원활용: 기술멘토링, 경영자문, 법률자문, 지자체 네트워크."
)

# === 4. Record builder ===
def make_record(tag, level, data):
    size = len(data)
    if size < 0xFFF:
        hdr = tag | (level << 10) | (size << 20)
        return struct.pack('<I', hdr) + data
    else:
        hdr = tag | (level << 10) | (0xFFF << 20)
        return struct.pack('<II', hdr, size) + data

# === 5. Rebuild body ===
# Strategy: For each empty PARA_HDR in content_map:
#   1. Modify PARA_HDR raw data to update nChars
#   2. Insert PARA_TXT record right after HDR (before existing CSH)
#   Empty cell structure: HDR -> CSH -> LSG -> ...
#   Filled cell structure: HDR -> TXT -> CSH -> LSG -> ...

new_body = bytearray()
for r in records:
    if r['i'] in content_map and r['tag'] == 66:
        # This is an empty PARA_HDR that needs content
        text = content_map[r['i']]
        nchars = len(text) + 1  # +1 for trailing CR
        nchars_with_flag = 0x80000000 | nchars

        # Modify PARA_HDR: update nChars (first 4 bytes of raw)
        new_raw = bytearray(r['raw'])
        struct.pack_into('<I', new_raw, 0, nchars_with_flag)

        # Write modified HDR
        new_body.extend(r['hdr'])
        new_body.extend(new_raw)

        # Insert PARA_TXT (tag 67) right after HDR
        txt_lvl = r['lvl'] + 1
        txt_data = text.encode('utf-16-le') + b'\x0d\x00'
        new_body.extend(make_record(67, txt_lvl, txt_data))
    else:
        # Write record as-is
        new_body.extend(r['hdr'])
        new_body.extend(r['raw'])

compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
new_compressed = compressor.compress(bytes(new_body)) + compressor.flush()
print(f"Body: {len(body)} -> {len(new_body)} bytes")
print(f"Compressed: {len(body_compressed)} -> {len(new_compressed)} bytes")

# === 6. OLE Mini-stream rewrite ===
shutil.copy2(SRC, DST)
with open(DST, 'rb') as f:
    fb = bytearray(f.read())

# Parse OLE header
dir_start = struct.unpack('<I', fb[48:52])[0]
minifat_start = struct.unpack('<I', fb[60:64])[0]

# DIFAT
difat = []
for j in range(109):
    val = struct.unpack('<I', fb[76+j*4:80+j*4])[0]
    if val != 0xFFFFFFFF and val != 0xFFFFFFFE:
        difat.append(val)

# Read FAT
fat = []
for fs in difat:
    off = (fs+1)*SECTOR_SIZE
    for j in range(128):
        fat.append(struct.unpack('<I', fb[off+j*4:off+j*4+4])[0])

# Read MiniFAT
mf_chain = []
s = minifat_start
while s != 0xFFFFFFFE and s != 0xFFFFFFFF and s < len(fat):
    mf_chain.append(s)
    s = fat[s]

minifat_data = bytearray()
for sec in mf_chain:
    off = (sec+1)*SECTOR_SIZE
    minifat_data.extend(fb[off:off+SECTOR_SIZE])

minifat = []
for j in range(len(minifat_data)//4):
    minifat.append(struct.unpack('<I', minifat_data[j*4:j*4+4])[0])

# Directory
dir_chain = []
s = dir_start
while s != 0xFFFFFFFE and s != 0xFFFFFFFF and s < len(fat):
    dir_chain.append(s)
    s = fat[s]

dir_data = bytearray()
for sec in dir_chain:
    off = (sec+1)*SECTOR_SIZE
    dir_data.extend(fb[off:off+SECTOR_SIZE])

# Root entry
root_start = struct.unpack('<I', dir_data[116:120])[0]
root_size = struct.unpack('<I', dir_data[120:124])[0]

# Find Section0
sec0_sid = None
for eid in range(len(dir_data)//128):
    entry_off = eid * 128
    entry_type = dir_data[entry_off + 66]
    if entry_type == 0: continue
    name_len = struct.unpack('<H', dir_data[entry_off+64:entry_off+66])[0]
    name_bytes = dir_data[entry_off:entry_off+name_len]
    try:
        name = name_bytes.decode('utf-16-le').rstrip('\x00')
    except:
        continue
    if name == 'Section0':
        sec0_sid = eid
        break

sec0_off = sec0_sid * 128
sec0_mini_start = struct.unpack('<I', dir_data[sec0_off+116:sec0_off+120])[0]

# Walk old mini-chain
old_mini_chain = []
s = sec0_mini_start
while s != 0xFFFFFFFE and s != 0xFFFFFFFF and s < len(minifat):
    old_mini_chain.append(s)
    s = minifat[s]

new_mini_needed = math.ceil(len(new_compressed) / MINI_SECTOR_SIZE)
old_mini_have = len(old_mini_chain)
print(f"Mini-sectors: need {new_mini_needed}, have {old_mini_have}")

# Root's regular sector chain
root_reg_chain = []
s = root_start
while s != 0xFFFFFFFE and s != 0xFFFFFFFF and s < len(fat):
    root_reg_chain.append(s)
    s = fat[s]

# Read mini-stream container
mini_stream = bytearray()
for sec in root_reg_chain:
    off = (sec+1)*SECTOR_SIZE
    mini_stream.extend(fb[off:off+SECTOR_SIZE])

# Build new mini-chain: reuse old, then allocate new
new_mini_chain = list(old_mini_chain[:min(old_mini_have, new_mini_needed)])

extra_mini = new_mini_needed - len(new_mini_chain)
if extra_mini > 0:
    # Find free mini-sectors
    used_minis = set(old_mini_chain)
    free_minis = [mi for mi in range(len(minifat)) if minifat[mi] == 0xFFFFFFFF and mi not in used_minis]
    for fm in free_minis:
        if extra_mini <= 0: break
        new_mini_chain.append(fm)
        extra_mini -= 1
    # Extend if still needed
    next_ms = len(minifat)
    while extra_mini > 0:
        new_mini_chain.append(next_ms)
        minifat.append(0xFFFFFFFF)
        next_ms += 1
        extra_mini -= 1

# Free unused old
if old_mini_have > new_mini_needed:
    for unused in old_mini_chain[new_mini_needed:]:
        minifat[unused] = 0xFFFFFFFF

# Update MiniFAT chain
for i, ms in enumerate(new_mini_chain):
    minifat[ms] = new_mini_chain[i+1] if i < len(new_mini_chain)-1 else 0xFFFFFFFE

print(f"New mini-chain: {len(new_mini_chain)} sectors")

# Ensure mini-stream is large enough
max_ms = max(new_mini_chain)
required_ms_size = (max_ms + 1) * MINI_SECTOR_SIZE
if len(mini_stream) < required_ms_size:
    mini_stream.extend(b'\x00' * (required_ms_size - len(mini_stream)))

# Write data to mini-sectors
for i, ms in enumerate(new_mini_chain):
    ms_off = ms * MINI_SECTOR_SIZE
    cs = i * MINI_SECTOR_SIZE
    ce = min(cs + MINI_SECTOR_SIZE, len(new_compressed))
    chunk = new_compressed[cs:ce]
    if len(chunk) < MINI_SECTOR_SIZE:
        chunk = chunk + b'\x00' * (MINI_SECTOR_SIZE - len(chunk))
    mini_stream[ms_off:ms_off+MINI_SECTOR_SIZE] = chunk

# Write mini-stream back to root's regular sectors
new_root_size = len(mini_stream)
root_secs_needed = math.ceil(new_root_size / SECTOR_SIZE)
root_secs_have = len(root_reg_chain)

new_root_chain = list(root_reg_chain[:min(root_secs_have, root_secs_needed)])
if root_secs_needed > root_secs_have:
    cur_file_secs = (len(fb) // SECTOR_SIZE) - 1
    for _ in range(root_secs_needed - root_secs_have):
        ns = cur_file_secs; cur_file_secs += 1
        fb.extend(b'\x00' * SECTOR_SIZE)
        while len(fat) <= ns: fat.append(0xFFFFFFFF)
        new_root_chain.append(ns)

if root_secs_have > root_secs_needed:
    for unused in root_reg_chain[root_secs_needed:]:
        fat[unused] = 0xFFFFFFFF

for i, sec in enumerate(new_root_chain):
    fat[sec] = new_root_chain[i+1] if i < len(new_root_chain)-1 else 0xFFFFFFFE

for i, sec in enumerate(new_root_chain):
    off = (sec+1)*SECTOR_SIZE
    cs = i * SECTOR_SIZE
    chunk = mini_stream[cs:cs+SECTOR_SIZE]
    if len(chunk) < SECTOR_SIZE: chunk += b'\x00'*(SECTOR_SIZE-len(chunk))
    while len(fb) < off+SECTOR_SIZE: fb.extend(b'\x00'*SECTOR_SIZE)
    fb[off:off+SECTOR_SIZE] = chunk

# Write MiniFAT back
new_mf_data = bytearray()
for val in minifat: new_mf_data.extend(struct.pack('<I', val))
while len(new_mf_data) % SECTOR_SIZE: new_mf_data.extend(b'\xff\xff\xff\xff')

mf_secs_needed = len(new_mf_data) // SECTOR_SIZE
mf_secs_have = len(mf_chain)
new_mf_chain = list(mf_chain[:min(mf_secs_have, mf_secs_needed)])
if mf_secs_needed > mf_secs_have:
    cur_file_secs = (len(fb) // SECTOR_SIZE) - 1
    for _ in range(mf_secs_needed - mf_secs_have):
        ns = cur_file_secs; cur_file_secs += 1
        fb.extend(b'\x00' * SECTOR_SIZE)
        while len(fat) <= ns: fat.append(0xFFFFFFFF)
        new_mf_chain.append(ns)

for i, sec in enumerate(new_mf_chain):
    fat[sec] = new_mf_chain[i+1] if i < len(new_mf_chain)-1 else 0xFFFFFFFE

for i, sec in enumerate(new_mf_chain):
    off = (sec+1)*SECTOR_SIZE
    fb[off:off+SECTOR_SIZE] = new_mf_data[i*SECTOR_SIZE:(i+1)*SECTOR_SIZE]

struct.pack_into('<I', fb, 60, new_mf_chain[0] if new_mf_chain else 0xFFFFFFFE)
struct.pack_into('<I', fb, 64, len(new_mf_chain))

# Update directory
dir_data2 = bytearray()
for sec in dir_chain:
    off = (sec+1)*SECTOR_SIZE
    dir_data2.extend(fb[off:off+SECTOR_SIZE])

# Section0: update start and size
struct.pack_into('<I', dir_data2, sec0_off+116, new_mini_chain[0])
struct.pack_into('<I', dir_data2, sec0_off+120, len(new_compressed))
# Root: update start and size
struct.pack_into('<I', dir_data2, 116, new_root_chain[0])
struct.pack_into('<I', dir_data2, 120, new_root_size)

for i, sec in enumerate(dir_chain):
    off = (sec+1)*SECTOR_SIZE
    fb[off:off+SECTOR_SIZE] = dir_data2[i*SECTOR_SIZE:(i+1)*SECTOR_SIZE]

# Write FAT
feps = SECTOR_SIZE // 4
fat_secs_needed = math.ceil(len(fat) / feps)
if fat_secs_needed > len(difat):
    cur_file_secs = (len(fb) // SECTOR_SIZE) - 1
    for _ in range(fat_secs_needed - len(difat)):
        ns = cur_file_secs; cur_file_secs += 1
        fb.extend(b'\x00' * SECTOR_SIZE)
        while len(fat) <= ns: fat.append(0xFFFFFFFF)
        fat[ns] = 0xFFFFFFFD
        difat.append(ns)
    struct.pack_into('<I', fb, 44, len(difat))
    for j in range(min(len(difat), 109)):
        struct.pack_into('<I', fb, 76+j*4, difat[j])

for fi, fs in enumerate(difat):
    off = (fs+1)*SECTOR_SIZE
    for j in range(feps):
        fidx = fi*feps + j
        val = fat[fidx] if fidx < len(fat) else 0xFFFFFFFF
        struct.pack_into('<I', fb, off+j*4, val & 0xFFFFFFFF)

with open(DST, 'wb') as f:
    f.write(fb)
print(f"\nFile written: {DST} ({len(fb)} bytes)")

# === 7. Verify ===
print("\n=== Verification ===")
try:
    ole_v = olefile.OleFileIO(DST)
    v_data = ole_v.openstream('BodyText/Section0').read()
    v_body = zlib.decompress(v_data, -15)
    print(f"Decompressed: {len(v_body)} bytes OK")

    # Parse and show text
    i = 0; texts = []
    while i < len(v_body):
        if i+4 > len(v_body): break
        hdr = struct.unpack('<I', v_body[i:i+4])[0]
        tag = hdr & 0x3FF; sz = (hdr >> 20) & 0xFFF
        if sz == 0xFFF:
            if i+8>len(v_body): break
            sz = struct.unpack('<I', v_body[i+4:i+8])[0]; i+=8
        else: i+=4
        if tag == 67:
            d = v_body[i:i+sz]; j=0; chars=[]
            while j<len(d)-1:
                ch=struct.unpack('<H',d[j:j+2])[0]
                if ch==0: break
                if ch<32:
                    if ch in (1,2,3,11,12,14,15,16,17,18,21,22,23): j+=16; continue
                    j+=2
                else: chars.append(chr(ch)); j+=2
            t=''.join(chars).strip()
            if t: texts.append(t)
        i+=sz

    print(f"\nTotal text blocks: {len(texts)}")
    for t in texts:
        print(f"  > {t[:100]}{'...' if len(t)>100 else ''}")
    ole_v.close()
    print("\nSUCCESS!")
except Exception as e:
    print(f"Verification FAILED: {e}")
    import traceback; traceback.print_exc()
