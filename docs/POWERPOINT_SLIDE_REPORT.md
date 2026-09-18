# EduGuard AI PowerPoint Slide Report

This report is generated from the current `/powerpoint` implementation: `services/presentation_service.py`, `templates/powerpoint.html`, `static/css/powerpoint.css`, `static/js/powerpoint.js`, and `data/reference/final_v2_metrics.json`. It describes the actual bilingual 20-slide deck. The viewer renders one active slide at a time and uses stored FINAL V2 evidence for dynamic metrics and charts.

## SLIDE 1

English title: EduGuard AI
Arabic title: EduGuard AI

Academic purpose: Introduce the graduation project and define the academic early-warning system.

Exact visible content:
- eyebrow: Graduation Project
- title: EduGuard AI
- subtitle: Student Academic Risk Early Warning System
- meta: Machine Learning / AI Decision Support System
- meta: NTI Graduation Project
- body: An academic early-warning system for evidence-based advisor support.

Arabic visible content:
- eyebrow: مشروع التخرج
- title: EduGuard AI
- subtitle: نظام الإنذار المبكر للمخاطر الأكاديمية للطلاب
- meta: نظام دعم قرار باستخدام تعلم الآلة والذكاء الاصطناعي
- meta: مشروع تخرج NTI
- body: نظام أكاديمي للإنذار المبكر ودعم المرشدين بقرارات قائمة على الأدلة.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Formal cover, subtitle, project metadata, and footer.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- No separate methodology is introduced on this slide.

Why this method:
- No separate method rationale is shown.

Important terminology:
- cover

What MUST be explained orally:
- Define early warning as support before a final outcome is resolved.
- Distinguish estimated risk from certainty.

Likely discussion questions:
- What is EduGuard AI?
- Who makes the final decision?

Source-supported answers:
- A Flask decision-support platform around an exported Semester-1 ML pipeline.
- The academic advisor remains responsible for the final decision.

Important warning:
- Never say the model guarantees dropout.

---

## SLIDE 2

English title: Project idea
Arabic title: فكرة المشروع

Academic purpose: Define the project idea as an early-warning decision-support workflow.

Exact visible content:
- title: Project idea
- lead: EduGuard AI is an early-warning decision-support system for universities.
- points: Identify students who may be academically at risk before the problem becomes severe.
- points: Estimate dropout risk from information available by the end of Semester 1.
- points: Give academic advisors an earlier, explainable basis for supportive intervention.
- diagram: Student information
- diagram: Estimated risk
- diagram: Advisor support

Arabic visible content:
- title: فكرة المشروع
- lead: EduGuard AI هو نظام لدعم القرار والإنذار المبكر في الجامعات.
- points: التعرف على الطلاب الذين قد يواجهون خطرًا أكاديميًا قبل تفاقم المشكلة.
- points: تقدير مخاطر الانسحاب باستخدام المعلومات المتاحة حتى نهاية الفصل الدراسي الأول.
- points: تزويد المرشد الأكاديمي أساسًا مبكرًا وقابلًا للتفسير للتدخل الداعم.
- diagram: بيانات الطالب
- diagram: المخاطر المقدّرة
- diagram: دعم المرشد

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Student information → Estimated risk → Advisor support flow.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- No separate methodology is introduced on this slide.

Why this method:
- No separate method rationale is shown.

Important terminology:
- idea

What MUST be explained orally:
- Explain why an early signal is useful before an outcome is known.
- Connect the output to supportive advising.

Likely discussion questions:
- What makes this early warning?
- What does the output represent?

Source-supported answers:
- The prediction point is the end of Semester 1.
- The output is a calibrated estimated probability with a band, review flag, explanations, and recommendations.

Important warning:
- Risk is not causality or certainty.

---

## SLIDE 3

English title: Problem statement
Arabic title: مشكلة البحث

Academic purpose: Present the academic problem and research question.

Exact visible content:
- title: Problem statement
- lead: Universities need a practical way to focus limited advising time on students who may need support first.
- points: Struggling students may be identified only after important opportunities for support have passed.
- points: Academic and financial indicators can provide an earlier warning signal.
- points: Manual monitoring becomes difficult as the number of students grows.
- points: Advisors need a data-driven support tool while retaining human judgment.
- question: Can information available by the end of Semester 1 identify students at risk of dropout?

Arabic visible content:
- title: مشكلة البحث
- lead: تحتاج الجامعات إلى طريقة عملية لتركيز وقت الإرشاد المحدود على الطلاب الذين قد يحتاجون إلى الدعم أولًا.
- points: قد يتم اكتشاف تعثر الطلاب بعد فوات فرص مهمة للدعم.
- points: يمكن أن توفر المؤشرات الأكاديمية والمالية إنذارًا مبكرًا.
- points: تصبح المتابعة اليدوية صعبة مع زيادة عدد الطلاب.
- points: يحتاج المرشدون إلى أداة قائمة على البيانات مع الحفاظ على الحكم البشري.
- question: هل يمكن استخدام المعلومات المتاحة حتى نهاية الفصل الدراسي الأول للتعرف على الطلاب المعرضين لخطر الانسحاب؟

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Bullets and highlighted research-question callout.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- No separate methodology is introduced on this slide.

Why this method:
- No separate method rationale is shown.

Important terminology:
- problem

What MUST be explained orally:
- Explain why manual monitoring of a large cohort is difficult.
- Read the research question exactly.

Likely discussion questions:
- Why is early identification difficult?

Source-supported answers:
- A large cohort makes consistent manual prioritization difficult; the system provides a repeatable aid while keeping human judgment.

Important warning:
- Data does not replace the advisor.

---

## SLIDE 4

English title: Project objectives
Arabic title: أهداف المشروع

Academic purpose: List the project objectives.

Exact visible content:
- title: Project objectives
- lead: The project combines a validated machine-learning workflow with a usable advisor interface.
- objectives: Build an early-warning machine-learning model.
- objectives: Predict dropout risk using data available by Semester 1.
- objectives: Prevent future-data leakage during model development.
- objectives: Provide calibrated risk scores rather than an uncalibrated ranking only.
- objectives: Explain individual predictions and generate advisor recommendations.
- objectives: Deliver a web-based decision-support system for analysis and reporting.

Arabic visible content:
- title: أهداف المشروع
- lead: يجمع المشروع بين سير عمل موثوق لتعلم الآلة وواجهة عملية للمرشد الأكاديمي.
- objectives: بناء نموذج تعلم آلة للإنذار المبكر.
- objectives: توقع مخاطر الانسحاب باستخدام بيانات الفصل الدراسي الأول.
- objectives: منع تسرب بيانات المستقبل أثناء التطوير.
- objectives: تقديم درجات مخاطر معايرة بدلًا من ترتيب غير معاير فقط.
- objectives: تفسير التنبؤات الفردية وتوليد توصيات للمرشد.
- objectives: تقديم نظام ويب لدعم القرار والتحليل والتقارير.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Six numbered objective blocks.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- No separate methodology is introduced on this slide.

Why this method:
- No separate method rationale is shown.

Important terminology:
- objectives

What MUST be explained orally:
- Explain leakage prevention and calibration as validity objectives.
- Connect explainability and recommendations to advisor usability.

Likely discussion questions:
- Which objective protects validity?
- Why include explainability?

Source-supported answers:
- Leakage prevention protects evaluation credibility; explanations let advisors inspect influential inputs.

Important warning:
- Objectives do not establish causality.

---

## SLIDE 5

English title: System scope
Arabic title: نطاق النظام

Academic purpose: Define the system boundary as decision support.

Exact visible content:
- title: System scope
- lead: EduGuard supports academic review; it does not replace an academic decision-maker.
- does: Estimate dropout risk
- does: Explain influential model inputs
- does: Rank students for review
- does: Support advisor follow-up
- does_not: Automatically expel students
- does_not: Make final academic decisions
- does_not: Prove that a factor caused dropout
- callout: Decision Support System

Arabic visible content:
- title: نطاق النظام
- lead: يدعم EduGuard المراجعة الأكاديمية ولا يحل محل صاحب القرار الأكاديمي.
- does: تقدير مخاطر الانسحاب
- does: تفسير المدخلات المؤثرة في النموذج
- does: ترتيب الطلاب للمراجعة
- does: دعم متابعة المرشد
- does_not: فصل الطلاب تلقائيًا
- does_not: اتخاذ القرارات الأكاديمية النهائية
- does_not: إثبات أن عاملًا ما تسبب في الانسحاب
- callout: نظام لدعم القرار

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Does/does-not panels and Decision Support System callout.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- No separate methodology is introduced on this slide.

Why this method:
- No separate method rationale is shown.

Important terminology:
- scope

What MUST be explained orally:
- Describe ranking and review as prioritization.
- Emphasize no automatic expulsion or final decision.

Likely discussion questions:
- Is this automated decision making?
- Can it expel a student?

Source-supported answers:
- No; it estimates risk and supports advisor review. No automatic punishment exists.

Important warning:
- Never present it as autonomous disciplinary software.

---

## SLIDE 6

English title: Dataset
Arabic title: بيانات الدراسة

Academic purpose: Describe the source cohort and original target categories.

Exact visible content:
- title: Dataset
- lead: The source contains demographic, admission, academic, financial and economic variables.
- source: UCI Machine Learning Repository
- why: The dataset provides a documented higher-education context for evaluating an early-warning approach.
- Students: 4,424
- Original input features: 36
- Original outcomes: 3
- Early-warning stages: 2

Arabic visible content:
- title: بيانات الدراسة
- lead: تتضمن البيانات متغيرات ديموغرافية ومتغيرات القبول والأداء الأكاديمي والتمويل والاقتصاد.
- source: مستودع UCI للتعلم الآلي
- why: توفر البيانات سياقًا موثقًا للتعليم العالي لتقييم منهج الإنذار المبكر.
- Students: 4,424
- Original input features: 36
- Original outcomes: 3
- Early-warning stages: 2

Numbers/metrics shown:
- `{"label": "Students", "value": 4424}`
- `{"label": "Original features", "value": 36}`
- `{"label": "Graduate", "value": 2209}`
- `{"label": "Dropout", "value": 1421}`
- `{"label": "Enrolled", "value": 794}`

Visual elements:
- Metric cards, outcome cards, source label, and dataset note.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Counts come from data/raw/data.csv; original input count is 36.

Why this method:
- The source provides demographic, admission, academic, financial, and economic context.

Important terminology:
- dataset

What MUST be explained orally:
- State 4,424 rows, 36 inputs, and three outcomes.
- Explain UCI provenance without claiming UCI collected the data.
- Differentiate original inputs from 30 operational features.

Likely discussion questions:
- How many students and variables?
- What are the outcomes?

Source-supported answers:
- There are 4,424 students, 36 inputs, Graduate 2,209, Dropout 1,421, and Enrolled 794.

Important warning:
- Do not call Enrolled a resolved negative label.

---

## SLIDE 7

English title: Target preparation
Arabic title: إعداد الهدف

Academic purpose: Explain the binary training target and separate current-student scoring cohort.

Exact visible content:
- title: Target preparation
- lead: The three original outcomes are separated into resolved training labels and a current-student scoring cohort.
- resolved: Graduate
- resolved: 0
- resolved: Dropout
- resolved: 1
- unresolved: Enrolled
- note: Enrolled is excluded from supervised training because it is not a resolved final outcome. After training, Enrolled students are scored by the model.
- why: This keeps the training target tied to outcomes that are known and resolved.

Arabic visible content:
- title: إعداد الهدف
- lead: يتم فصل الحالات النهائية الأصلية إلى تسميات تدريب محسومة ومجموعة طلاب حاليين للتقييم.
- resolved: خريج
- resolved: 0
- resolved: منسحب من الدراسة
- resolved: 1
- unresolved: مقيد حاليًا
- note: يُستبعد الطلاب المقيدون من التدريب الخاضع للإشراف لأن حالتهم ليست نتيجة نهائية محسومة. بعد التدريب، يقيّم النموذج الطلاب المقيدين.
- why: يربط هذا الإجراء هدف التدريب بنتائج معروفة ومحسومة.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Graduate→0, Dropout→1, and Enrolled-not-training cards.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- Training uses resolved Graduate/Dropout rows; Enrolled is scored after training.

Why this method:
- Enrolled is unresolved, so relabeling it would invent an outcome.

Important terminology:
- target

What MUST be explained orally:
- Mention 3,630 resolved and 794 Enrolled rows.
- Clarify Student ID and name are not model features.

Likely discussion questions:
- Why not train on Enrolled?
- What happens to Enrolled?

Source-supported answers:
- Enrolled has no final outcome at the prediction point; the trained binary model scores the current students.

Important warning:
- Do not describe Enrolled as class 0 or a confirmed graduate.

---

## SLIDE 8

English title: Early-warning design and data leakage
Arabic title: تصميم الإنذار المبكر ومنع تسرب البيانات

Academic purpose: Show the end-of-Semester-1 prediction point and prevent future-data leakage.

Exact visible content:
- title: Early-warning design and data leakage
- lead: The prediction point is the end of Semester 1.
- allowed: Enrollment information
- allowed: Admission and background information
- allowed: Financial and economic context
- allowed: Semester-1 performance
- excluded: Semester-2 credited units
- excluded: Semester-2 enrolled units
- excluded: Semester-2 evaluations
- excluded: Semester-2 approved units
- excluded: Semester-2 grade
- excluded: Semester-2 units without evaluation
- note: Semester-2 variables contain future information relative to the decision point. Keeping them would make evaluation unrealistically strong.
- why: Removing future information makes the early-warning experiment match the information available when an advisor would act.

Arabic visible content:
- title: تصميم الإنذار المبكر ومنع تسرب البيانات
- lead: تحدث عملية التنبؤ في نهاية الفصل الدراسي الأول.
- allowed: معلومات الالتحاق
- allowed: معلومات القبول والخلفية
- allowed: السياق المالي والاقتصادي
- allowed: أداء الفصل الدراسي الأول
- excluded: الوحدات المحتسبة في الفصل الثاني
- excluded: الوحدات المسجلة في الفصل الثاني
- excluded: تقييمات الفصل الثاني
- excluded: الوحدات المجتازة في الفصل الثاني
- excluded: درجة الفصل الثاني
- excluded: وحدات الفصل الثاني دون تقييم
- note: تحتوي متغيرات الفصل الثاني على معلومات مستقبلية بالنسبة إلى نقطة القرار. استخدامها يجعل التقييم قويًا بشكل غير واقعي.
- why: استبعاد معلومات المستقبل يجعل التجربة مطابقة للمعلومات المتاحة عند اتخاذ قرار الدعم.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Allowed/excluded panels for Semester 1 and Semester 2.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- Six Semester-2 columns are excluded: credited, enrolled, evaluations, approved, grade, and without evaluations.

Why this method:
- Semester-2 values are future information and would make evaluation unrealistically strong.

Important terminology:
- leakage

What MUST be explained orally:
- Name the prediction point.
- Explain leakage.
- State that six columns were removed, leaving 30 operational features.

Likely discussion questions:
- What is leakage here?
- Why not use Semester 2?

Source-supported answers:
- Leakage uses information unavailable when an advisor would act; Semester 2 would no longer test an early-warning system.

Important warning:
- Do not claim the operational model uses Semester-2 inputs.

---

## SLIDE 9

English title: Data preprocessing
Arabic title: المعالجة المسبقة للبيانات

Academic purpose: Document data-quality checks and preprocessing.

Exact visible content:
- title: Data preprocessing
- lead: The validation workflow checks data quality before fitting any candidate model.
- pipeline: Raw data
- pipeline: Quality check
- pipeline: Duplicate check
- pipeline: Invalid-value validation
- pipeline: Feature typing
- pipeline: Encoding
- pipeline: Scaling where required
- points: Categorical features are One-Hot Encoded.
- points: Numeric missing values use median imputation.
- points: Categorical missing values use most-frequent imputation.
- why: A fixed preprocessing pipeline applies the same data preparation rules during training and inference.

Arabic visible content:
- title: المعالجة المسبقة للبيانات
- lead: يتحقق سير العمل من جودة البيانات قبل تدريب أي نموذج مرشح.
- pipeline: البيانات الخام
- pipeline: فحص الجودة
- pipeline: فحص التكرار
- pipeline: التحقق من القيم غير الصالحة
- pipeline: تحديد نوع الخصائص
- pipeline: الترميز
- pipeline: القياس عند الحاجة
- points: يتم ترميز الخصائص الفئوية باستخدام One-Hot Encoding.
- points: تستخدم القيم الوسيطة لتعويض القيم الرقمية المفقودة.
- points: تستخدم الفئة الأكثر تكرارًا لتعويض القيم الفئوية المفقودة.
- why: يطبق خط معالجة ثابت قواعد التحضير نفسها أثناء التدريب والاستخدام.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Seven-node raw-data-to-scaling pipeline.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- FINAL V2 reports zero missing values and zero duplicates before drop; categorical features are one-hot encoded and imputed by the pipeline.

Why this method:
- A fixed pipeline applies the same rules during training and inference.

Important terminology:
- preprocessing

What MUST be explained orally:
- Explain median and most-frequent imputation.
- Explain one-hot encoding and validation.

Likely discussion questions:
- How are missing values handled?
- Why use a pipeline?

Source-supported answers:
- Numeric values use median imputation and categorical values most-frequent imputation; the pipeline keeps transformations consistent.

Important warning:
- Do not claim missingness was ignored.

---

## SLIDE 10

English title: Outlier handling
Arabic title: معالجة القيم الشاذة

Academic purpose: Explain why extreme values were inspected but not deleted blindly.

Exact visible content:
- title: Outlier handling
- lead: Outlier detection is used to inspect values, not to delete students mechanically.
- points: IQR analysis identified many extreme observations.
- points: Older students, unusual unit counts and extreme but valid grades can be legitimate records.
- points: Impossible values are treated as missing and validated before modeling.
- points: Valid extreme observations remain in the dataset.
- methods: Logistic Regression: RobustScaler
- methods: Tree models: original numeric scale
- why: RobustScaler uses the median and IQR, so it is less affected by extreme values; tree models do not require scaling.

Arabic visible content:
- title: معالجة القيم الشاذة
- lead: يُستخدم اكتشاف القيم الشاذة لفحص البيانات، وليس لحذف الطلاب آليًا.
- points: كشف تحليل IQR عن عدد كبير من القيم المتطرفة.
- points: قد تكون أعمار بعض الطلاب أو أعداد الوحدات أو الدرجات المتطرفة صحيحة.
- points: تُعامل القيم المستحيلة كقيم مفقودة وتخضع للتحقق.
- points: تبقى الملاحظات المتطرفة الصحيحة في البيانات.
- methods: الانحدار اللوجستي: RobustScaler
- methods: نماذج الأشجار: المقياس الرقمي الأصلي
- why: يستخدم RobustScaler الوسيط وIQR، لذلك يتأثر بدرجة أقل بالقيم المتطرفة؛ ولا تحتاج نماذج الأشجار إلى القياس.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Outlier bullets and RobustScaler/tree-model choices.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- IQR detects unusual values; impossible values become missing; valid extremes remain. Logistic Regression uses RobustScaler; tree models keep numeric scale.

Why this method:
- Median/IQR scaling is less sensitive to valid extremes, while tree splits do not require scaling.

Important terminology:
- outliers

What MUST be explained orally:
- Give valid extreme examples.
- Contrast RobustScaler with StandardScaler.
- Explain why tree models do not need scaling.

Likely discussion questions:
- Why not remove all IQR outliers?
- Which model receives RobustScaler?

Source-supported answers:
- IQR does not prove invalidity; only Logistic Regression uses RobustScaler in this design.

Important warning:
- Do not say all IQR outliers were deleted.

---

## SLIDE 11

English title: Class imbalance
Arabic title: عدم توازن الفئات

Academic purpose: Describe class imbalance and handling.

Exact visible content:
- title: Class imbalance
- lead: The resolved outcomes are not perfectly balanced, so the training objective accounts for class frequency.
- handling: class_weight for Logistic Regression, Random Forest and Extra Trees
- handling: scale_pos_weight for XGBoost
- why: Class weighting preserves real student records while giving the positive Dropout class appropriate influence.
- smote: SMOTE was not required: class weighting was sufficient and avoids creating synthetic student records.

Arabic visible content:
- title: عدم توازن الفئات
- lead: النتائج المحسومة ليست متوازنة تمامًا، لذلك يراعي التدريب تكرار الفئات.
- handling: class_weight للانحدار اللوجستي وRandom Forest وExtra Trees
- handling: scale_pos_weight لنموذج XGBoost
- why: يحافظ وزن الفئات على سجلات الطلاب الحقيقية ويمنح فئة الانسحاب تأثيرًا مناسبًا.
- smote: لم تكن SMOTE مطلوبة؛ كان وزن الفئات كافيًا وتجنب إنشاء سجلات طلاب اصطناعية.

Numbers/metrics shown:
- `{"label": "Graduate", "value": 2209}`
- `{"label": "Dropout", "value": 1421}`
- `{"label": "scale_pos_weight", "value": 1.5527472527472528}`

Visual elements:
- Graduate/Dropout cards, bars, class-weight chips, and SMOTE note.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Resolved counts are 2,209 Graduate and 1,421 Dropout; training counts are 1,413 and 910 with scale_pos_weight 1.5527472527472528.

Why this method:
- Class weighting preserves real records and gives Dropout suitable influence; SMOTE was not required.

Important terminology:
- imbalance

What MUST be explained orally:
- Explain Dropout as the positive class.
- Explain class_weight and scale_pos_weight.
- Explain why synthetic records were avoided.

Likely discussion questions:
- Why not SMOTE?
- What is scale_pos_weight?

Source-supported answers:
- Class weighting was sufficient and avoids synthetic student records; scale_pos_weight weights the positive class.

Important warning:
- Do not claim perfect balance or SMOTE usage.

---

## SLIDE 12

English title: Models evaluated
Arabic title: النماذج التي تم تقييمها

Academic purpose: Compare four candidate classifiers and cross-validated PR-AUC.

Exact visible content:
- title: Models evaluated
- lead: Four complementary classifiers were compared with the same evaluation design.
- model_notes: Logistic Regression
- model_notes: Simple, interpretable baseline
- model_notes: Random Forest
- model_notes: Non-linear ensemble
- model_notes: Extra Trees
- model_notes: High-randomness ensemble comparison
- model_notes: XGBoost
- model_notes: Gradient boosting model for tabular data
- why: Comparing a linear baseline with three tree ensembles tests whether non-linear relationships improve early-warning performance.
- XGBoost: CV PR-AUC 92.77%
- Logistic Regression: CV PR-AUC 92.39%
- Random Forest: CV PR-AUC 91.83%
- Extra Trees: CV PR-AUC 89.60%
- Selected model highlighted: XGBoost

Arabic visible content:
- title: النماذج التي تم تقييمها
- lead: تمت مقارنة أربعة مصنفات متكاملة باستخدام تصميم التقييم نفسه.
- model_notes: Logistic Regression
- model_notes: خط أساس بسيط قابل للتفسير
- model_notes: Random Forest
- model_notes: تجميع غير خطي
- model_notes: Extra Trees
- model_notes: مقارنة بتجميع عالي العشوائية
- model_notes: XGBoost
- model_notes: تعزيز تدريجي للبيانات الجدولية
- why: تختبر مقارنة خط أساس خطي مع ثلاثة نماذج أشجار ما إذا كانت العلاقات غير الخطية تحسن الإنذار المبكر.
- XGBoost: CV PR-AUC 92.77%
- Logistic Regression: CV PR-AUC 92.39%
- Random Forest: CV PR-AUC 91.83%
- Extra Trees: CV PR-AUC 89.60%
- Selected model highlighted: XGBoost

Numbers/metrics shown:
- `{"model": "XGBoost", "cv_pr_auc": 0.9276638343, "selected": true}`
- `{"model": "Logistic Regression", "cv_pr_auc": 0.9238844665, "selected": false}`
- `{"model": "Random Forest", "cv_pr_auc": 0.9182875735, "selected": false}`
- `{"model": "Extra Trees", "cv_pr_auc": 0.8959963732, "selected": false}`

Visual elements:
- Horizontal Chart.js chart and four model-note cards; XGBoost highlighted.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- CV PR-AUC values come from final_v2_metrics.json.

Why this method:
- The comparison covers an interpretable baseline and complementary tree ensembles for nonlinear tabular data.

Important terminology:
- models

What MUST be explained orally:
- Explain the baseline.
- Contrast ensemble families.
- Point out evidence-based selection.

Likely discussion questions:
- Why include Logistic Regression?
- Why include XGBoost?

Source-supported answers:
- Logistic Regression is a transparent baseline; XGBoost is a strong tabular candidate and had the strongest CV PR-AUC in this run.

Important warning:
- Do not say XGBoost is universally best.

---

## SLIDE 13

English title: Model selection and cross-validation
Arabic title: اختيار النموذج والتحقق المتقاطع

Academic purpose: Explain five-fold Stratified CV, PR-AUC selection, and the train/CV gap.

Exact visible content:
- title: Model selection and cross-validation
- lead: Model selection uses five-fold Stratified Cross-Validation on the resolved training population.
- selection_metric: PR-AUC
- points: Stratification preserves the Graduate/Dropout class distribution in each fold.
- points: PR-AUC focuses on the positive Dropout class and is informative under class imbalance.
- points: XGBoost achieved the strongest cross-validated PR-AUC and was selected.
- note: There is a moderate Train-to-CV gap of approximately 5.9 percentage points, while validation and untouched test performance remain strong.
- why: Stratified cross-validation preserves class proportions across folds; PR-AUC focuses evaluation on the positive Dropout class under class imbalance.
- Train PR-AUC: 98.66%
- CV PR-AUC: 92.77%
- Train/CV gap: 5.90 percentage points
- Selected model: XGBoost

Arabic visible content:
- title: اختيار النموذج والتحقق المتقاطع
- lead: استخدم اختيار النموذج تحققًا متقاطعًا طبقيًا من خمس طيات على مجموعة التدريب المحسومة.
- selection_metric: PR-AUC
- points: يحافظ التقسيم الطبقي على توزيع فئتي التخرج والانسحاب في كل طية.
- points: يركز PR-AUC على فئة الانسحاب الإيجابية ويُعد مناسبًا مع عدم توازن الفئات.
- points: حقق XGBoost أقوى PR-AUC متقاطع وتم اختياره.
- why: يقدر التحقق الطبقي التعميم مع الحفاظ على نسب الفئات؛ ويركز PR-AUC على الفئة التي تحتاج إلى دعم مبكر.
- Train PR-AUC: 98.66%
- CV PR-AUC: 92.77%
- Train/CV gap: 5.90 percentage points
- Selected model: XGBoost

Numbers/metrics shown:
- `{"label": "Selected model", "value": "XGBoost"}`
- `{"label": "Train PR-AUC", "value": 0.9866443336008119}`
- `{"label": "CV PR-AUC", "value": 0.9276638343041993}`
- `{"label": "Train/CV gap", "value": 0.05898049929661264}`

Visual elements:
- Selection cards, grouped train/CV chart, and rationale bullets.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Five-fold Stratified Cross-Validation; PR-AUC is primary selection metric; all four models are shown.

Why this method:
- Stratification preserves class proportions; PR-AUC focuses Dropout; XGBoost had the strongest CV PR-AUC.

Important terminology:
- selection

What MUST be explained orally:
- Read Train 98.66%, CV 92.77%, gap 5.90 percentage points.
- Use moderate-gap wording.
- Explain strong untouched-test evidence.

Likely discussion questions:
- Why PR-AUC instead of accuracy?
- Does the gap prove overfitting?

Source-supported answers:
- PR-AUC focuses precision/recall for the positive class; the moderate gap is monitored while CV and test performance remain strong.

Important warning:
- Do not call the gap negligible.

---

## SLIDE 14

English title: Probability calibration and threshold
Arabic title: معايرة الاحتمالات والحدود

Academic purpose: Explain isotonic calibration, thresholds, and human review.

Exact visible content:
- title: Probability calibration and threshold
- lead: The selected model is calibrated so the displayed score is easier to interpret as estimated risk.
- calibrator: Isotonic Regression
- points: High-risk threshold: selected to meet a minimum target Recall of 85%.
- points: Medium-risk threshold: 30%.
- points: Human-review margin: ±8 percentage points around the high-risk threshold.
- why: Calibration improves the interpretation of probabilities; threshold tuning makes the early-warning system sensitive to the positive class.
- High-risk threshold: 48.15%
- Medium-risk threshold: 30.00%
- Review margin: ±8.00%

Arabic visible content:
- title: معايرة الاحتمالات والحدود
- lead: تمت معايرة النموذج المختار ليكون تفسير الدرجة المعروضة أقرب إلى المخاطر المقدّرة.
- calibrator: Isotonic Regression
- points: حد المخاطر المرتفعة: اختير لتحقيق حد أدنى للاستدعاء قدره 85٪.
- points: حد المخاطر المتوسطة: 30٪.
- points: هامش المراجعة البشرية: ±8 نقاط مئوية حول حد المخاطر المرتفعة.
- why: تحسن المعايرة تفسير الاحتمالات؛ ويجعل ضبط العتبة النظام أكثر حساسية للفئة الإيجابية.
- High-risk threshold: 48.15%
- Medium-risk threshold: 30.00%
- Review margin: ±8.00%

Numbers/metrics shown:
- `{"label": "High threshold", "value": 0.48148149251937866}`
- `{"label": "Medium threshold", "value": 0.3}`
- `{"label": "Review margin", "value": 0.08}`

Visual elements:
- Isotonic label, threshold scale, cards, and bullets.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- High threshold 0.48148149251937866; medium threshold 0.3; review margin 0.08.

Why this method:
- Isotonic Regression makes scores more interpretable as estimated probabilities; high threshold tuning targeted minimum Recall 85%.

Important terminology:
- calibration

What MUST be explained orally:
- Explain calibration as probability interpretation.
- Explain bands and separate review margin.

Likely discussion questions:
- Why Isotonic Regression?
- How was high threshold chosen?

Source-supported answers:
- It calibrates raw scores; threshold tuning targeted minimum Recall 85% and exported 0.48148149251937866.

Important warning:
- 48.15% remains estimated risk, not certainty.

---

## SLIDE 15

English title: Final test results
Arabic title: النتائج النهائية للاختبار

Academic purpose: Present final untouched-test metrics and emphasize Recall.

Exact visible content:
- title: Final test results
- lead: These values come from the untouched FINAL V2 test split after model selection and calibration.
- why: Recall is emphasized because missing a student who may need support can be more costly than reviewing additional false-positive cases.
- Accuracy: 86.91%
- Precision: 78.21%
- Recall: 92.25%
- F1: 84.65%
- PR-AUC: 93.78%
- ROC-AUC: 95.31%
- Brier Score: 0.07753758132457733

Arabic visible content:
- title: النتائج النهائية للاختبار
- lead: تأتي هذه القيم من مجموعة اختبار FINAL V2 غير المستخدمة بعد اختيار النموذج والمعايرة.
- why: يحظى الاستدعاء باهتمام خاص لأن تفويت طالب قد يحتاج إلى الدعم قد يكون أكثر تكلفة من مراجعة حالات إيجابية كاذبة إضافية.
- Accuracy: 86.91%
- Precision: 78.21%
- Recall: 92.25%
- F1: 84.65%
- PR-AUC: 93.78%
- ROC-AUC: 95.31%
- Brier Score: 0.07753758132457733

Numbers/metrics shown:
- `{"label": "Accuracy", "value": 0.8691460055096418}`
- `{"label": "Precision", "value": 0.7820895522388059}`
- `{"label": "Recall", "value": 0.9225352112676056}`
- `{"label": "F1", "value": 0.8465266558966075}`
- `{"label": "PR-AUC", "value": 0.9377955609524928}`
- `{"label": "ROC-AUC", "value": 0.9531180294436301}`
- `{"label": "Brier Score", "value": 0.07753758132457733}`

Visual elements:
- Seven metric cards with Recall emphasized.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Values are from the untouched FINAL V2 test split after selection and calibration.

Why this method:
- Missing an at-risk student can cost more than reviewing additional false positives.

Important terminology:
- performance

What MUST be explained orally:
- Read all metrics.
- Explain Brier Score as probabilistic squared-error quality.
- State these are test values.

Likely discussion questions:
- What does Brier Score mean?
- Why is Recall important?

Source-supported answers:
- Brier Score summarizes probability error; the executed value is 0.07753758132457733. Recall is central to early warning.

Important warning:
- Do not present Brier as accuracy or claim perfection.

---

## SLIDE 16

English title: Model evaluation
Arabic title: تقييم النموذج

Academic purpose: Show confusion-matrix, ranking, calibration, and confidence-interval evidence.

Exact visible content:
- title: Model evaluation
- lead: The final test probabilities were evaluated with threshold, ranking and calibration views.
- labels: Confusion Matrix
- labels: ROC Curve
- labels: Precision–Recall Curve
- labels: Calibration Curve
- labels: 95% Confidence Intervals
- interpretation: The stored curves and intervals are derived from the executed FINAL V2 run; no curve points are invented for the presentation.
- Confusion matrix: [[369, 73], [22, 262]]
- PR-AUC 95% CI: 0.9161018266–0.9555469419
- ROC-AUC 95% CI: 0.9359615383–0.9684400573
- Recall 95% CI: 0.8892757937–0.9555612245
- Precision 95% CI: 0.7380240667–0.8272782406
- F1 95% CI: 0.8148148148–0.8760488981

Arabic visible content:
- title: تقييم النموذج
- lead: تم تقييم احتمالات الاختبار النهائية باستخدام مصفوفة الالتباس ومنحنيات الترتيب والمعايرة.
- labels: مصفوفة الالتباس
- labels: منحنى ROC
- labels: منحنى Precision–Recall
- labels: منحنى المعايرة
- labels: فواصل الثقة 95٪
- interpretation: تم اشتقاق المنحنيات والفواصل المخزنة من تشغيل FINAL V2 الفعلي؛ ولم تتم إضافة نقاط منحنيات مختلقة.
- Confusion matrix: [[369, 73], [22, 262]]
- PR-AUC 95% CI: 0.9161018266–0.9555469419
- ROC-AUC 95% CI: 0.9359615383–0.9684400573
- Recall 95% CI: 0.8892757937–0.9555612245
- Precision 95% CI: 0.7380240667–0.8272782406
- F1 95% CI: 0.8148148148–0.8760488981

Numbers/metrics shown:
- `{"label": "Confusion matrix", "value": [[369, 73], [22, 262]]}`
- `{"label": "PR-AUC", "estimate": 0.9385347632, "95% CI low": 0.9161018266, "95% CI high": 0.9555469419}`
- `{"label": "ROC-AUC", "estimate": 0.9536915262, "95% CI low": 0.9359615383, "95% CI high": 0.9684400573}`
- `{"label": "Recall", "estimate": 0.923351306, "95% CI low": 0.8892757937, "95% CI high": 0.9555612245}`
- `{"label": "Precision", "estimate": 0.782234957, "95% CI low": 0.7380240667, "95% CI high": 0.8272782406}`
- `{"label": "F1", "estimate": 0.8470974885, "95% CI low": 0.8148148148, "95% CI high": 0.8760488981}`

Visual elements:
- Confusion cards, 95% CI rows, and stored ROC, PR, and calibration curves.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Charts use actual curve arrays in final_v2_metrics.json; no points are invented.

Why this method:
- Multiple views separate classification errors, ranking quality, and probability reliability.

Important terminology:
- evaluation

What MUST be explained orally:
- Explain each matrix cell.
- Explain ROC-AUC versus PR-AUC.
- Explain confidence intervals.

Likely discussion questions:
- What does the matrix show?
- How do ROC-AUC and PR-AUC differ?

Source-supported answers:
- The matrix is [[369, 73], [22, 262]]. ROC-AUC summarizes both classes; PR-AUC focuses the positive Dropout class.

Important warning:
- AUC is not threshold-specific accuracy or causal evidence.

---

## SLIDE 17

English title: Feature importance and explainability
Arabic title: أهمية الخصائص وقابلية التفسير

Academic purpose: Distinguish global feature importance from SHAP contribution.

Exact visible content:
- title: Feature importance and explainability
- lead: Global importance and local contribution answer different questions about the model.
- definitions: Permutation Importance
- definitions: Global effect on model performance when a feature is shuffled.
- definitions: SHAP
- definitions: Contribution of features to an individual or global prediction.
- definitions: Caution
- definitions: A model contribution does not prove causation.
- features: Curricular units 1st sem (approved)
- features: Curricular units 1st sem (enrolled)
- features: Tuition fees up to date
- features: Course
- features: Curricular units 1st sem (grade)
- features: Scholarship holder
- features: Debtor
- why: Using both global and local explanations helps an advisor understand model behavior without presenting it as a causal finding.

Arabic visible content:
- title: أهمية الخصائص وقابلية التفسير
- lead: تجيب الأهمية العامة والمساهمة المحلية عن سؤالين مختلفين حول سلوك النموذج.
- definitions: Permutation Importance
- definitions: الأثر العام على أداء النموذج عند تبديل قيم الخاصية.
- definitions: SHAP
- definitions: مساهمة الخصائص في تنبؤ فردي أو في النموذج عمومًا.
- definitions: تنبيه
- definitions: مساهمة النموذج لا تثبت علاقة سببية.
- features: الوحدات المجتازة في الفصل الأول
- features: الوحدات المسجلة في الفصل الأول
- features: انتظام المصروفات الدراسية
- features: التخصص
- features: درجة الفصل الأول
- features: الحصول على منحة
- features: وجود مستحقات مالية
- why: يساعد الجمع بين التفسير العام والمحلي المرشد على فهم سلوك النموذج دون عرضه كاكتشاف سببي.

Numbers/metrics shown:
- `{"type": "Permutation Importance", "feature": "Curricular units 1st sem (approved)", "value": 0.2852187992}`
- `{"type": "Permutation Importance", "feature": "Curricular units 1st sem (enrolled)", "value": 0.042846897}`
- `{"type": "Permutation Importance", "feature": "Tuition fees up to date", "value": 0.031834553}`
- `{"type": "Permutation Importance", "feature": "Course", "value": 0.0149714717}`
- `{"type": "Permutation Importance", "feature": "Scholarship holder", "value": 0.0051729909}`
- `{"type": "SHAP Mean |SHAP|", "feature": "Curricular units 1st sem (approved)", "value": 1.6268441677}`
- `{"type": "SHAP Mean |SHAP|", "feature": "Tuition fees up to date", "value": 0.4464859068}`
- `{"type": "SHAP Mean |SHAP|", "feature": "Curricular units 1st sem (grade)", "value": 0.3937901855}`
- `{"type": "SHAP Mean |SHAP|", "feature": "Course", "value": 0.3803649247}`
- `{"type": "SHAP Mean |SHAP|", "feature": "Curricular units 1st sem (enrolled)", "value": 0.3502492309}`

Visual elements:
- Definition cards, top-five permutation bars, top-five SHAP bars, and feature note.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Permutation and SHAP summaries come from final_v2_metrics.json; Flask computes Tree SHAP for individual inputs.

Why this method:
- The views show global sensitivity and contribution without causal claims.

Important terminology:
- explainability

What MUST be explained orally:
- Explain shuffling for permutation importance.
- Explain SHAP contribution.
- Mention leading features and individual direction.

Likely discussion questions:
- Feature importance versus SHAP?
- Does SHAP prove causation?

Source-supported answers:
- Permutation measures performance change after shuffling; SHAP attributes contribution. Neither proves causation.

Important warning:
- Do not say a feature caused dropout.

---

## SLIDE 18

English title: Risk scoring current students
Arabic title: تقييم مخاطر الطلاب المقيدين حاليًا

Academic purpose: Report calibrated risk bands for the current Enrolled cohort.

Exact visible content:
- title: Risk scoring current students
- lead: The trained model scores the current Enrolled cohort after supervised training is complete.
- note: The Medium-risk band exists, but no student in this scored cohort falls inside that calibrated probability interval. This is a cohort result, not a system error.
- Enrolled: 794
- Low: 309
- Medium: 0
- High: 485
- Human Review: 140

Arabic visible content:
- title: تقييم مخاطر الطلاب المقيدين حاليًا
- lead: يقيّم النموذج المدرب مجموعة الطلاب المقيدين بعد اكتمال التدريب الخاضع للإشراف.
- note: توجد فئة المخاطر المتوسطة في النظام، لكن لا يقع أي طالب في هذه المجموعة داخل مجال الاحتمال المعاير لها. هذه نتيجة للمجموعة وليست خطأ في النظام.
- Enrolled: 794
- Low: 309
- Medium: 0
- High: 485
- Human Review: 140

Numbers/metrics shown:
- `{"label": "Enrolled", "value": 794}`
- `{"label": "Low", "value": 309}`
- `{"label": "Medium", "value": 0}`
- `{"label": "High", "value": 485}`
- `{"label": "Human Review", "value": 140}`

Visual elements:
- Four cards, risk bars, review count, and Medium=0 note.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.
- `data/reference/final_v2_metrics.json` for the listed metrics.

Methodology explained:
- Counts are actual FINAL V2 Enrolled scoring results.

Why this method:
- Scoring Enrolled after training gives a current review population without inventing resolved labels.

Important terminology:
- enrolled

What MUST be explained orally:
- Read 794 total, 309 Low, 0 Medium, 485 High, 140 review.
- Explain Medium=0 as a cohort result.
- Explain review can overlap bands.

Likely discussion questions:
- Why is Medium zero?
- Does High mean dropout?

Source-supported answers:
- No current score falls inside Medium; High is an estimated prioritization band, not a certain outcome.

Important warning:
- Do not call High students confirmed dropouts.

---

## SLIDE 19

English title: Advisor recommendation engine
Arabic title: محرك توصيات المرشد الأكاديمي

Academic purpose: Show how risk and explanations become advisor recommendations.

Exact visible content:
- title: Advisor recommendation engine
- lead: EduGuard connects the risk estimate to observable, actionable academic and financial signals.
- steps: Risk score
- steps: Explanation
- steps: Actionable signals
- steps: Advisor recommendation
- actions: Targeted tutoring
- actions: Advisor meeting
- actions: Missed-assessment review
- actions: Financial support
- actions: Payment-plan review
- note: Sensitive characteristics are not used as intervention reasons.

Arabic visible content:
- title: محرك توصيات المرشد الأكاديمي
- lead: يربط EduGuard تقدير المخاطر بإشارات أكاديمية ومالية قابلة للتدخل.
- steps: درجة المخاطر
- steps: التفسير
- steps: الإشارات القابلة للتدخل
- steps: توصية المرشد
- actions: دعم دراسي موجه
- actions: اجتماع مع المرشد
- actions: مراجعة التقييمات الفائتة
- actions: دعم مالي
- actions: مراجعة خطة السداد
- note: لا تستخدم الخصائص الحساسة كأسباب للتدخل.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Four-step flow and five action chips.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- Recommendations are generated by rule-based recommendations() from Semester-1 academic and financial signals.

Why this method:
- Transparent rules keep actions traceable and separate from model probability.

Important terminology:
- recommendations

What MUST be explained orally:
- Give examples: low approval, low grade, missed evaluations, arrears, debtor, scholarship eligibility.
- Emphasize supportive action.
- Sensitive characteristics are not intervention reasons.

Likely discussion questions:
- Why rules?
- What triggers financial support?

Source-supported answers:
- The service maps observable signals to transparent actions; tuition/debtor/scholarship status can trigger support guidance.

Important warning:
- Recommendations are not mandatory or causal findings.

---

## SLIDE 20

English title: Complete system and conclusion
Arabic title: النظام الكامل والخلاصة

Academic purpose: Close with the full platform flow and academic conclusion.

Exact visible content:
- title: Complete system and conclusion
- lead: The result is an end-to-end academic decision-support workflow.
- system: Dataset
- system: ML model
- system: Calibrated risk
- system: SHAP explanation
- system: Advisor recommendations
- system: Flask application
- system: Dashboard / reports / bulk upload
- conclusion: EduGuard demonstrates that information available by the end of Semester 1 can provide a strong early-warning signal for student dropout risk.
- closing: Earlier detection. Explainable estimates. Actionable advisor support.

Arabic visible content:
- title: النظام الكامل والخلاصة
- lead: النتيجة هي سير عمل متكامل لدعم القرار الأكاديمي.
- system: البيانات
- system: نموذج تعلم الآلة
- system: المخاطر المعايرة
- system: تفسير SHAP
- system: توصيات المرشد
- system: تطبيق Flask
- system: لوحة التحكم والتقارير والرفع الجماعي
- conclusion: يوضح EduGuard أن المعلومات المتاحة حتى نهاية الفصل الدراسي الأول يمكن أن تقدم إشارة إنذار مبكر قوية لمخاطر انسحاب الطلاب.
- closing: اكتشاف أبكر. تقديرات قابلة للتفسير. دعم عملي للمرشد.

Numbers/metrics shown:
- No FINAL V2 metric card is shown.

Visual elements:
- Seven-node flow from Dataset to Flask and dashboard/reports/bulk upload.

Data source:
- `services/presentation_service.py` for catalog and static narrative.
- `static/js/powerpoint.js` for dynamic rendering and Chart.js.

Methodology explained:
- The slide combines current Flask routes, artifacts, explanations, recommendations, and reporting.

Why this method:
- The end-to-end path shows how validated evidence becomes a usable advisor tool.

Important terminology:
- conclusion

What MUST be explained orally:
- Walk from data to artifact to Flask pages.
- Re-state human judgment.
- Summarize detection, calibration, explanation, and action.

Likely discussion questions:
- What is the contribution?
- What is needed before deployment?

Source-supported answers:
- The project demonstrates a Semester-1 early-warning workflow connected to an explainable Flask application; institutional validation and governance remain necessary.

Important warning:
- Do not claim universal generalization or autonomous decisions.

---

# Presentation Master Summary

## 1. Presentation objective

Present EduGuard AI as an academic end-to-end early-warning decision-support system: a validated end-of-Semester-1 ML experiment connected to calibrated risk, explanation, advisor recommendations, and a bilingual Flask application.

## 2. Full slide order

1. EduGuard AI / EduGuard AI
2. Project idea / فكرة المشروع
3. Problem statement / مشكلة البحث
4. Project objectives / أهداف المشروع
5. System scope / نطاق النظام
6. Dataset / بيانات الدراسة
7. Target preparation / إعداد الهدف
8. Early-warning design and data leakage / تصميم الإنذار المبكر ومنع تسرب البيانات
9. Data preprocessing / المعالجة المسبقة للبيانات
10. Outlier handling / معالجة القيم الشاذة
11. Class imbalance / عدم توازن الفئات
12. Models evaluated / النماذج التي تم تقييمها
13. Model selection and cross-validation / اختيار النموذج والتحقق المتقاطع
14. Probability calibration and threshold / معايرة الاحتمالات والحدود
15. Final test results / النتائج النهائية للاختبار
16. Model evaluation / تقييم النموذج
17. Feature importance and explainability / أهمية الخصائص وقابلية التفسير
18. Risk scoring current students / تقييم مخاطر الطلاب المقيدين حاليًا
19. Advisor recommendation engine / محرك توصيات المرشد الأكاديمي
20. Complete system and conclusion / النظام الكامل والخلاصة

## 3. Total slides

20

## 4. Total presentation flow

Problem → Objective → Data → Methodology → Modeling → Validation → Explainability → Risk scoring → Recommendations → System → Conclusion

## 5. Exact FINAL V2 metrics used in the slides

| Metric | Executed value |
|---|---:|
| Selected Model | XGBoost |
| Train PR-AUC | 0.9866443336008119 |
| CV PR-AUC | 0.9276638343041993 |
| Train/CV gap | 0.05898049929661264 |
| Accuracy | 0.8691460055096418 |
| Precision | 0.7820895522388059 |
| Recall | 0.9225352112676056 |
| F1 | 0.8465266558966075 |
| PR-AUC | 0.9377955609524928 |
| ROC-AUC | 0.9531180294436301 |
| Brier | 0.07753758132457733 |
| High threshold | 0.48148149251937866 |
| Medium threshold | 0.3 |
| Review margin | 0.08 |
| Enrolled | 794 |
| Low | 309 |
| Medium | 0 |
| High | 485 |
| Human Review | 140 |

The viewer formats percentages to two decimal places; this table preserves executed precision.

## Evidence boundaries

- SHAP contributions are associations, not causal effects or percentage-point changes.
- Recommendations are transparent rule logic, not causal model findings.
- EduGuard is Decision Support; advisors decide what support is appropriate.
- No slide supports a claim that a student will certainly drop out or that one source generalizes to every university.
