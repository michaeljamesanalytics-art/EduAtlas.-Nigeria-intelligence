#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/curated.json'
d=json.loads(p.read_text(encoding='utf-8'))
NEW=[
('nbte-office','National Board for Technical Education','Technical education regulation and accreditation','National Board for Technical Education','National','Technical and vocational programme oversight, standards, and accredited institutions.','Which programmes in this location have active accreditation?','https://www.nbte.gov.ng/','Regulators'),
('ncce-office','National Commission for Colleges of Education','Teacher education regulatory institution','National Commission for Colleges of Education','National','Quality assurance, curriculum and standards associated with colleges of education.','Which teacher education programmes meet applicable minimum standards?','https://ncce.gov.ng/Home/ActsAndFunctions','Regulators'),
('neco-office','National Examinations Council','Nigerian examination administration','National Examinations Council','National','Administration of specified national school examinations, including NECO senior secondary and basic education certification examinations.','Which examinations, candidate categories and assessment methods are covered?','https://neco.gov.ng/','Assessment & certification'),
('nelfund-office','Nigerian Education Loan Fund','Student financing institution','Nigerian Education Loan Fund','National','Administration of eligible education loans, including student support disbursements subject to programme rules.','What has been applied for, approved, actually disbursed and sustained?','https://nelf.gov.ng/','Finance & implementation'),
('state-ministry-office','State Ministries of Education (vary by state)','State education policy and administration','36 State Ministries of Education / FCT education authorities','State / FCT','State-level administration, school policy execution, personnel and financing responsibilities, varying by state and education level.','Which state office has authority over this school or programme?','https://education.gov.ng/','Implementation'),
('local-education-office','Local Government Education Authorities','Local basic education administration','Local Government Education Authorities','Local','School support, supervision and implementation through applicable state/local arrangements.','Who supervises school attendance, facilities and basic education delivery in this LGA?','https://ubec.gov.ng/','Implementation'),
('headteacher-office','Public school leaders and management committees','School-level governance and instructional leadership','Individual schools','School','School planning, teaching support, safeguarding, reporting, management and appropriate family engagement.','What evidence does this school retain on attendance, teaching conditions and improvement?','https://emis.education.gov.ng/','Implementation'),
('nerdc-curriculum-unit','NERDC official curriculum resources','Curriculum framework and resource publication','Nigerian Educational Research and Development Council','National','Official curriculum framework development and publication of implementation-related educational materials.','Which curriculum version and subject framework applies to this school year?','https://nerdc.gov.ng/','Standards & curriculum'),
('budget-execution','Federal budget implementation reporting','Federal fiscal performance records','Budget Office of the Federation','National','Quarterly fiscal implementation reporting relevant to federal education vote execution.','Which actual releases and expenditures support the project figure?','https://budgetoffice.gov.ng/index.php/resources/internal-resources/reports/quarterly-budget-implementation','Finance & implementation'),
]
existing={x['id'] for x in d['stakeholders']}
for x in NEW:
 if x[0] in existing:continue
 d['stakeholders'].append(dict(zip(['id','person','role','organization','scope','responsibility','question','url','category'],x)))
for x in [
 {'name':'National Commission for Colleges of Education','type':'Teacher education and accreditation','url':'https://ncce.gov.ng/Home/ActsAndFunctions'},
 {'name':'National Board for Technical Education','type':'Technical education regulation and accreditation','url':'https://www.nbte.gov.ng/'},
 {'name':'National Examinations Council','type':'School examinations and certification','url':'https://neco.gov.ng/'},
 {'name':'Nigerian Education Loan Fund','type':'Tertiary student loans','url':'https://nelf.gov.ng/'},
 {'name':'World Bank Global Education Evidence Advisory Panel','type':'Impact evidence and cost-effectiveness','url':'https://www.worldbank.org/en/brief/2025/10/30/global-education-evidence-advisory-panel'},
]:
 if x['url'] not in {s['url'] for s in d['sources']}:d['sources'].append(x)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'data/curated.js').write_text('window.EDUATLAS='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print('stakeholders',len(d['stakeholders']),'source entries',len(d['sources']))
