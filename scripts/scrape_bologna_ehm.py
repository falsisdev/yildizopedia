import os
import re
import ssl
import json
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()

def get_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        return BeautifulSoup(resp.read(), 'html.parser')

def parse_course_page(course_url):
    try:
        soup = get_soup(course_url)
        tables = soup.find_all('table')
        if not tables:
            return None
        
        info = {'url': course_url}
        # Table 0: Name, Code, Credit, ECTS, hours
        t0_rows = tables[0].find_all('tr')
        if len(t0_rows) >= 2:
            cols = [td.get_text(strip=True) for td in t0_rows[1].find_all(['td', 'th'])]
            if len(cols) >= 5:
                info['name'] = cols[0]
                info['code'] = cols[1]
                info['credit'] = cols[2]
                info['ects'] = cols[3]
                info['lecture_hours'] = cols[4]
            if len(cols) >= 7:
                info['app_hours'] = cols[5]
                info['lab_hours'] = cols[6]

        # Table 1: Prerequisites
        if len(tables) > 1:
            t1_tds = tables[1].find_all(['td', 'th'])
            if len(t1_tds) >= 2:
                info['prerequisites'] = t1_tds[1].get_text(strip=True)
            else:
                info['prerequisites'] = tables[1].get_text(strip=True)

        # Table 2: Semester
        if len(tables) > 2:
            t2_tds = tables[2].find_all(['td', 'th'])
            if len(t2_tds) >= 2:
                info['semester'] = t2_tds[1].get_text(strip=True)

        # Table 3: Language & Course Type
        if len(tables) > 3:
            t3_text = tables[3].get_text(" ", strip=True)
            info['details_raw'] = t3_text

        # Table 5: Objective & Content
        if len(tables) > 5:
            t5_rows = tables[5].find_all('tr')
            for r in t5_rows:
                tds = r.find_all(['td', 'th'])
                if len(tds) >= 2:
                    header = tds[0].get_text(strip=True)
                    val = tds[1].get_text(strip=True)
                    if 'Amacı' in header:
                        info['objective'] = val
                    elif 'İçeriği' in header:
                        info['content'] = val

        # Table 7: Weekly plan
        weekly_plan = []
        for t in tables:
            th_list = [th.get_text(strip=True) for th in t.find_all('th')]
            if any('Hafta' in th for th in th_list) and any('Konular' in th for th in th_list):
                for r in t.find_all('tr')[1:]:
                    tds = r.find_all('td')
                    if len(tds) >= 2:
                        w_num = tds[0].get_text(strip=True)
                        w_topic = tds[1].get_text(strip=True)
                        weekly_plan.append({'week': w_num, 'topic': w_topic})
                break
        info['weekly_plan'] = weekly_plan

        # Assessment / Değerlendirme
        assessments = []
        for t in tables:
            th_list = [th.get_text(strip=True) for th in t.find_all('th')]
            if any('Etkinlikler' in th for th in th_list) and any('Katkı Payı' in th for th in th_list):
                for r in t.find_all('tr')[1:]:
                    tds = r.find_all('td')
                    if len(tds) >= 3:
                        act = tds[0].get_text(strip=True)
                        count = tds[1].get_text(strip=True)
                        weight = tds[2].get_text(strip=True)
                        if act and weight:
                            assessments.append({'activity': act, 'count': count, 'weight': weight})
                break
        info['assessments'] = assessments

        return info
    except Exception as e:
        print(f"Error parsing course {course_url}: {e}")
        return None

def main():
    bologna_url = "https://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=6&aid=5"
    print("Fetching Bologna main curriculum page...")
    soup = get_soup(bologna_url)
    tables = soup.find_all('table')
    t2 = tables[2]

    semesters = {}
    current_sem_name = "1. Yarıyıl"
    sem_counter = 1

    for tr in t2.find_all('tr'):
        th = tr.find('th')
        if th and ('Yarıyıl' in th.get_text() or 'Yıl' in th.get_text()):
            raw_title = th.get_text(strip=True)
            current_sem_name = f"{sem_counter}. Yarıyıl ({raw_title})"
            semesters[current_sem_name] = []
            sem_counter += 1
            continue

        tds = tr.find_all('td')
        if len(tds) >= 8:
            code = tds[0].get_text(strip=True)
            prereq = tds[1].get_text(strip=True)
            name = tds[2].get_text(strip=True)
            theory = tds[3].get_text(strip=True)
            app = tds[4].get_text(strip=True)
            lab = tds[5].get_text(strip=True)
            credit = tds[6].get_text(strip=True)
            ects = tds[7].get_text(strip=True)
            a_tag = tds[0].find('a') or tr.find('a')
            course_link = urljoin(bologna_url, a_tag['href']) if a_tag and a_tag.get('href') else ''

            if current_sem_name not in semesters:
                semesters[current_sem_name] = []

            semesters[current_sem_name].append({
                'code': code,
                'prereq': prereq,
                'name': name,
                'theory': theory,
                'app': app,
                'lab': lab,
                'credit': credit,
                'ects': ects,
                'link': course_link
            })

    print(f"Parsed {len(semesters)} semester groups.")
    
    # Save raw curriculum structure
    with open('scripts/bologna_ehm_raw.json', 'w', encoding='utf-8') as f:
        json.dump(semesters, f, ensure_ascii=False, indent=2)
    print("Saved scripts/bologna_ehm_raw.json")

    # Fetch detailed data for courses in semesters 1-7, and mandatory/sample courses in semester 8
    detailed_courses = {}
    for sem_name, course_list in list(semesters.items())[:7]:
        print(f"\nFetching details for {sem_name} ({len(course_list)} courses)...")
        for c in course_list:
            if c['link'] and c['code'] not in detailed_courses:
                print(f"  Fetching: {c['code']} - {c['name']}...")
                c_info = parse_course_page(c['link'])
                if c_info:
                    c.update(c_info)
                    detailed_courses[c['code']] = c

    # In sem 8 (4. Yıl Bahar), fetch mandatory courses: EHM4012, EHM9000, TDB1032
    if len(semesters) >= 8:
        sem8_name = list(semesters.keys())[7]
        sem8_courses = semesters[sem8_name]
        print(f"\nFetching mandatory & core elective details for {sem8_name}...")
        for c in sem8_courses[:15]:  # Fetch mandatory + top technical electives
            if c['link'] and c['code'] not in detailed_courses:
                print(f"  Fetching: {c['code']} - {c['name']}...")
                c_info = parse_course_page(c['link'])
                if c_info:
                    c.update(c_info)
                    detailed_courses[c['code']] = c

    with open('scripts/bologna_ehm_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(semesters, f, ensure_ascii=False, indent=2)
    print("\nSaved scripts/bologna_ehm_detailed.json successfully!")

if __name__ == '__main__':
    main()
