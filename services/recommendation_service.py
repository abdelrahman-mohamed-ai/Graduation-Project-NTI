S1 = 'Curricular units 1st sem'


def recommendations(f):
    actions = []
    enrolled, approved = f[f'{S1} (enrolled)'], f[f'{S1} (approved)']
    if enrolled and approved / enrolled < .5:
        actions += ['Schedule an urgent academic-advisor meeting to review progression.',
                    'Arrange tutoring for unapproved curricular units.']
    if f[f'{S1} (grade)'] < 10:
        actions.append('Agree a study plan and schedule a follow-up with academic support.')
    if f[f'{S1} (without evaluations)'] > 0:
        actions.append('Review missed assessments and discuss barriers with the student.')
    if not f['Tuition fees up to date']:
        actions.append('Refer to financial support to review outstanding tuition fees.')
    if f['Debtor']:
        actions.append('Offer financial counseling and explore a feasible payment plan.')
    if (f['Debtor'] or not f['Tuition fees up to date']) and not f['Scholarship holder']:
        actions.append('Review eligibility for scholarships or emergency financial aid.')
    return actions or ['Continue routine monitoring and agree the next progress check with the student.']


def snapshot(f):
    enrolled = f[f'{S1} (enrolled)']
    return {'Admission grade': f['Admission grade'],
            'Previous qualification grade': f['Previous qualification (grade)'],
            'Semester-1 grade': f[f'{S1} (grade)'],
            'Enrolled units': enrolled, 'Approved units': f[f'{S1} (approved)'],
            'Approval rate': round(f[f'{S1} (approved)'] / enrolled * 100, 1) if enrolled else None,
            'Evaluations': f[f'{S1} (evaluations)'],
            'Units without evaluations': f[f'{S1} (without evaluations)']}
