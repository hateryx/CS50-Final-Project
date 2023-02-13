import re
import titlecase


def title_builder(title):
    match = re.search(r"/.+/(\d{2}/\d{2}/\d{2}/)(.+)", title)
    if match:
        date = match.group(1)
        snippet = match.group(2)
    x = snippet.replace("-", " ")
    f_title = titlecase.titlecase(x)

    return f_title


case_1 = "/news/02/14/23/china-blames-ph-coast-guard-over-laser-incident-near-ayungin-shoal"
case_2 = "/news/02/13/23/panukalang-center-for-disease-prevention-nasa-plenaryo-na-ng-senado"

print(
    title_builder(case_1),
    title_builder(case_2)
)
