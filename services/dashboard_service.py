from collections import Counter, defaultdict


def dashboard(repo, model):
    students = repo.query(all_rows=True)['students']
    analyzed = [s for s in students if s['risk_probability'] is not None]
    counts = Counter(s['risk_level'] for s in analyzed)
    courses, histogram = defaultdict(list), [0] * 10
    for s in analyzed:
        courses[model.course(s['course_code'])].append(s['risk_score'])
        histogram[min(int(s['risk_score'] // 10), 9)] += 1
    return {'total': len(students), 'analyzed': len(analyzed), 'counts': {k: counts[k] for k in ('High', 'Medium', 'Low')},
        'average': round(sum(s['risk_score'] for s in analyzed) / len(analyzed), 1) if analyzed else None,
        'review': sum(s['manual_review'] for s in analyzed), 'histogram': histogram,
        'courses': sorted([{'course': k, 'average': round(sum(v) / len(v), 1), 'count': len(v)} for k, v in courses.items()], key=lambda x: -x['average']),
        'importance': model.importance[:8]}
