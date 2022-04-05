# web config
web_config = {
    'job_indeed': {
        'web_url': 'https://pk.indeed.com',
        'name': 'job_indeed',
        'search_page': {
            'input_field': '#text-input-what',
            'press_enter': True,
            'url_search': False
        },
        'result_page': {
            'results_container': 'html',
            'links': '.resultWithShelf',
            'next_page': '.pagination-list > li:nth-child(6) > a:nth-child(1)'
        },
        'job_page': {
            'job_title': '.icl-u-xs-mb--xs',
            'company_name': '.icl-u-lg-mr--sm',
            'email': '--no_css_found--',
            'city': '.icl-u-textColor--secondary > div:nth-child(2)',
            'p-osted_by': '.icl-u-lg-mr--sm'
        },
        'accept_cookies': {'accept': '#onetrust-accept-btn-handler'}
    }
}