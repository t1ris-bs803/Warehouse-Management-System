# 모듈 불러오기 #
import os, json, csv
from datetime import datetime


# 하드코딩 정보 #
name = "테스트회사"
########################


# CSV 데이터 정리 #
def write_log(action, product, count, from_pos="", to_pos=""):
    filename = "log.csv"
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["시간", "종류", "제품", "수량", "출발위치", "도착위치"])

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, action, product, count, from_pos, to_pos])
########################
   

# DB 데이터 정리 #
def load_data(filename="storage.json"):
    if not os.path.exists(filename):
        return {}

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data, filename="storage.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
########################


# 창고정리 시스템 #
def storage_add(position, product, count):
    data = load_data()

    if position not in data:
        data[position] = {}

    if product in data[position]:
        data[position][product] += count
    else:
        data[position][product] = count

    save_data(data)
    return True

def storage_remove(position, product, count):
    data = load_data()

    if position not in data or product not in data[position]:
        print("\n❌ 해당 위치에 제품이 없습니다.")
        return False

    if data[position][product] < count:
        print("\n❌ 재고가 부족합니다.")
        return False

    data[position][product] -= count

    if data[position][product] == 0:
        del data[position][product]
        if not data[position]:
            del data[position]

    save_data(data)
    return True

def storage_move(from_pos, to_pos, product, count):
    data = load_data()

    if from_pos not in data or product not in data[from_pos]:
        print("\n❌ 출발 위치에 해당 제품이 없습니다.")
        return False

    if data[from_pos][product] < count:
        print("\n❌ 이동할 수량이 부족합니다.")
        return False

    if to_pos not in data:
        data[to_pos] = {}

    data[from_pos][product] -= count
    data[to_pos][product] = data[to_pos].get(product, 0) + count

    if data[from_pos][product] == 0:
        del data[from_pos][product]
        if not data[from_pos]:
            del data[from_pos]

    save_data(data)
    return True

def storage_info(product):
    data = load_data()
    total = 0
    found = False

    print(f"\n📦 제품명: {product}")

    for position, items in data.items():
        if product in items:
            qty = items[product]
            print(f" - 위치 {position}: {qty}개")
            total += qty
            found = True

    if found:
        print(f"\n✅ 총 재고 수량: {total}개")
    else:
        print("❌ 해당 제품은 창고에 없습니다.")
########################


# 실행 #
print(f"[+] 반갑습니다.\n\n    {name}\n    창고정리 시스템입니다.")
input("\nEnter to start")
while True:
    print("\n\n\n\n\n\n\n\n\n\n1. 추가\n2. 제거\n3. 이동\n4. 확인\n5. 종료\n\n제품 위치는 '창고-층/세로/가로' 로 입력바랍니다.")
    
    try:
        choose = int(input("숫자를 입력해주세요: ").strip())

    except ValueError:
        print("\n❌ 1~5 사이 숫자를 입력해주세요.")
        input("Enter to continue")
        continue

    if choose == 1:
        product = input("\n입고할 제품 이름을 입력해주세요: ").strip()
        position = input("제품을 보관할 위치를 적어주세요: ").strip()
        try:
            count = int(input("입고할 수량을 입력해주세요: ").strip())

        except ValueError:
            print("\n❌ 수량은 숫자로 입력해주세요.")
            input("Enter to return")
            continue

        if count <= 0:
            print("\n❌ 수량은 1 이상이어야 합니다.")
            input("Enter to return")
            continue

        success = storage_add(position, product, count)
        if success:
            print(f"\n✅ {product} {count}개를 {position}에 입고했습니다.")
            write_log("입고", product, count, "", position)
        input("Enter to return")

    elif choose == 2:
        product = input("출고할 제품 이름을 입력해주세요: ").strip()
        position = input("제품이 보관되어 있던 위치를 적어주세요: ").strip()
        try:
            count = int(input("출고할 수량을 입력해주세요: ").strip())

        except ValueError:
            print("\n❌ 수량은 숫자로 입력해주세요.")
            input("Enter to return")
            continue

        if count <= 0:
            print("\n❌ 수량은 1 이상이어야 합니다.")
            input("Enter to return")
            continue

        success = storage_remove(position, product, count)
        if success:
            print(f"\n✅ {product} {count}개를 {position}에서 출고했습니다.")
            write_log("출고", product, count, position, "")
        input("Enter to return")

    elif choose == 3:
        product = input("\n이동할 제품 이름을 입력해주세요: ").strip()
        from_pos = input("현재 보관되어 있는 위치를 입력해주세요: ").strip()
        to_pos = input("이후 보관할 위치를 입력해주세요: ").strip()

        try:
            count = int(input("이동할 수량: ").strip())
        except ValueError:
            print("❌ 수량은 숫자로 입력해주세요.")
            input("Enter to return")
            continue

        success = storage_move(from_pos, to_pos, product, count)
        if success:
            print(f"\n✅ {product} {count}개를 {from_pos} → {to_pos}로 이동했습니다.")
            write_log("이동", product, count, from_pos, to_pos)
        input("Enter to return")

    elif choose == 4:
        product = input("\n확인하고 싶은 제품을 입력하세요: ")
        storage_info(product)
        input("\nEnter to return")

    elif choose == 5:
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n[-] 안녕히가십시오.\n\n    {name}\n    창고정리 시스템\n")
        break

    else:
        print("\n❌ 1~5 사이 숫자를 입력해주세요.")
        input("Enter to continue")
        continue
########################
