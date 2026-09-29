with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Header: Add "+ Upload Product" button right next to Admin and Cart
idx_orders = html.find("navigate('orders')")
idx_orders_end = html.find('</button>', idx_orders) + 9

new_upload_btn = '''\n\n                    <!-- Direct Upload Product Action Button -->
                    <a href="#admin" onclick="navigate('admin'); switchAdminTab('add-product');" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-400 via-amber-500 to-yellow-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-xs shadow-md shadow-amber-500/25 hover:shadow-amber-500/40 hover:scale-[1.02] transition-all" title="Upload your own products to Next Vision Brand">
                        <i data-lucide="plus-circle" class="w-4 h-4 text-slate-950"></i>
                        <span>+ Upload Product</span>
                    </a>'''

html = html[:idx_orders_end] + new_upload_btn + html[idx_orders_end:]
print("Added + Upload Product button to header")

# 2. Top announcement bar: update "Sell on NVB" link to direct to Add Product
old_sell_link = '<a href="#seller" onclick="navigate(\'seller\')" class="hover:text-blue-400 transition">Sell on NVB</a>'
new_sell_link = '<a href="#admin" onclick="navigate(\'admin\'); switchAdminTab(\'add-product\');" class="text-amber-400 hover:text-amber-300 font-bold transition flex items-center gap-1"><i data-lucide="plus-circle" class="w-3.5 h-3.5"></i> + Upload Product (பொருட்கள் பதிவேற்ற)</a>'

if old_sell_link in html:
    html = html.replace(old_sell_link, new_sell_link)
    print("Replaced Sell on NVB with Upload Product link in top bar")

# 3. Replace handleAdminAddProduct with robust version
idx_h = html.find('async function handleAdminAddProduct')
idx_h_end = html.find('function downloadCSVTemplate', idx_h)

new_add_handler = '''async function handleAdminAddProduct(e) {
            if (e) e.preventDefault();
            const title = document.getElementById('add-prod-title').value.trim();
            const catVal = document.getElementById('add-prod-cat').value.trim();
            const subcategory = document.getElementById('add-prod-subcat').value.trim() || 'General';
            const brand = document.getElementById('add-prod-brand').value.trim() || 'Next Vision Brand';
            const sku = document.getElementById('add-prod-sku').value.trim();
            const price = parseFloat(document.getElementById('add-prod-price').value);
            const mrp = parseFloat(document.getElementById('add-prod-mrp').value) || (price * 1.25);
            const stock = parseInt(document.getElementById('add-prod-stock').value) || 25;
            const short_desc = document.getElementById('add-prod-short-desc').value.trim();
            const description = document.getElementById('add-prod-desc').value.trim() || short_desc;
            const imgUrl = document.getElementById('add-prod-img-url').value.trim() || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800';
            const specsRaw = document.getElementById('add-prod-specs').value.trim();
            const is_featured = document.getElementById('add-prod-feat').checked;
            const is_flash = document.getElementById('add-prod-flash').checked;
            const is_deal = document.getElementById('add-prod-deal').checked;

            if (!title) {
                showToast('Please enter the Product Title (பொருளின் பெயரை உள்ளிடவும்).', 'error');
                return;
            }
            if (isNaN(price) || price <= 0) {
                showToast('Please enter a valid Selling Price (சரியான விற்பனை விலையை உள்ளிடவும்).', 'error');
                return;
            }

            let specsObj = {};
            if (specsRaw) {
                try {
                    specsObj = JSON.parse(specsRaw);
                } catch (err) {
                    const lines = specsRaw.split('\\n');
                    lines.forEach(l => {
                        const parts = l.split(':');
                        if (parts.length >= 2) {
                            specsObj[parts[0].trim()] = parts.slice(1).join(':').trim();
                        }
                    });
                    if (Object.keys(specsObj).length === 0) {
                        specsObj = { "Feature": specsRaw };
                    }
                }
            } else {
                specsObj = { "Brand": brand, "Category": catVal };
            }

            const payload = {
                title: title,
                category: catVal,
                category_id: 1,
                subcategory: subcategory,
                brand: brand,
                sku: sku || ('NVB-' + Math.floor(1000 + Math.random() * 9000)),
                price: price,
                mrp: mrp,
                stock: stock,
                short_description: short_desc || (title + ' by ' + brand),
                description: description,
                image_url: imgUrl,
                additional_images: [imgUrl],
                specifications: specsObj,
                variants: [],
                is_featured: is_featured,
                is_flash_sale: is_flash,
                deal_of_the_day: is_deal,
                rating: 5.0,
                reviews_count: 0
            };

            try {
                showToast('Publishing product to store...', 'info');
                const res = await fetch('/api/admin/products', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (res.ok) {
                    showToast(`Product "${title}" published successfully! (தயாரிப்பு வெற்றிகரமாக பதிவேற்றப்பட்டது)`, 'success');
                    // Reset inputs
                    document.getElementById('add-prod-title').value = '';
                    document.getElementById('add-prod-price').value = '';
                    document.getElementById('add-prod-mrp').value = '';
                    document.getElementById('add-prod-stock').value = '25';
                    document.getElementById('add-prod-short-desc').value = '';
                    document.getElementById('add-prod-desc').value = '';
                    document.getElementById('add-prod-specs').value = '';
                    document.getElementById('add-prod-img-url').value = '';
                    const preview = document.getElementById('image-preview-container');
                    if (preview) preview.innerHTML = '<span class="text-xs text-slate-500">Image Preview</span>';

                    await fetchProducts();
                    loadAdminProductsTable();

                    // Open the product detail page directly so the user sees it live!
                    if (data.id) {
                        setTimeout(() => {
                            openProductDetail(data.id);
                        }, 1200);
                    }
                } else {
                    showToast(data.detail || 'Failed to add product.', 'error');
                }
            } catch (err) {
                console.error(err);
                showToast('Network error while creating product.', 'error');
            }
        }\n\n        // ==========================================\n        // SECTION 38: BULK CSV IMPORT ENGINE\n        // ==========================================\n        '''

if idx_h != -1 and idx_h_end != -1:
    html = html[:idx_h] + new_add_handler + html[idx_h_end:]
    print("Replaced handleAdminAddProduct with robust version")
else:
    print("Warning: handleAdminAddProduct range not found")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("patch_upload_ui2 applied successfully!")
