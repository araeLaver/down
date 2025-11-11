#!/bin/bash

# Add navigation to business_discovery.html
sed -i '561 a\        <!-- Navigation -->\n        <div style="margin-bottom: 1.5rem;">\n            <a href="/business-discovery" style="display: inline-block; padding: 0.5rem 1rem; background: #6366f1; color: white; text-decoration: none; border-radius: 8px; margin-right: 0.5rem; border: 1px solid #6366f1;">\n                <i class="fas fa-trophy"></i> 우수 사업 (80+)\n            </a>\n            <a href="/business-review" style="display: inline-block; padding: 0.5rem 1rem; background: white; color: #6b7280; text-decoration: none; border-radius: 8px; margin-right: 0.5rem; border: 1px solid var(--border-color);">\n                <i class="fas fa-clipboard-check"></i> 검토 필요 (60-79)\n            </a>\n            <a href="/business-rejected" style="display: inline-block; padding: 0.5rem 1rem; background: white; color: #6b7280; text-decoration: none; border-radius: 8px; margin-right: 0.5rem; border: 1px solid var(--border-color);">\n                <i class="fas fa-times-circle"></i> 부적합 (60 미만)\n            </a>\n        </div>\n' templates/business_discovery.html

echo "Navigation added!"
