with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add "+ Upload Product" button in header
header_btn_old = '''<button onclick="navigate('orders')" class="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-slate-300 hover:text-white hover:bg-white/5 transition text-xs font-semibold">
                        <i data-lucide="package" class="w-4 h-4"></i>
                        <span>Orders</span>
                    </button>'''

header_btn_new = '''<button onclick="navigate('orders')" class="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-slate-300 hover:text-white hover:bg-white/5 transition text-xs font-semibold">
                        <i data-lucide="package" class="w-4 h-4"></i>
                        <span>Orders</span>
                    </button>

                    <!-- Direct Upload Product Action Button -->
                    <a href="#admin" onclick="navigate('admin'); switchAdminTab('add-product');" class="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-amber-400 via-amber-500 to-yellow-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-xs shadow-lg shadow-amber-500/25 hover:shadow-amber-500/40 hover:scale-[1.02] transition-all duration-200" title="Upload your own products to Next Vision Brand">
                        <i data-lucide="plus-circle" class="w-4 h-4"></i>
                        <span>+ Upload Product</span>
                    </a>'''

if header_btn_old in html:
    html = html.replace(header_btn_old, header_btn_new)
    print("Added Upload Product button to header")
else:
    print("Warning: header_btn_old not matched")

# 2. Add Upload Product button to Mobile Drawer
mobile_btn_old = '''                    <a href="#seller" onclick="navigate('seller'); toggleMobileNav();" class="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 text-slate-300 hover:text-white font-medium">
                        <i data-lucide="briefcase" class="w-5 h-5 text-indigo-400"></i>
                        <span>Seller Portal</span>
                    </a>'''

mobile_btn_new = '''                    <a href="#admin" onclick="toggleMobileNav(); navigate('admin'); switchAdminTab('add-product');" class="flex items-center gap-3 p-3 rounded-xl bg-gradient-to-r from-amber-500/20 to-yellow-500/10 border border-amber-500/30 text-amber-300 font-bold text-sm">
                        <i data-lucide="plus-circle" class="w-5 h-5 text-amber-400"></i>
                        <span>+ Upload Your Products (பொருட்கள் பதிவேற்ற)</span>
                    </a>

                    <a href="#seller" onclick="navigate('seller'); toggleMobileNav();" class="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 text-slate-300 hover:text-white font-medium">
                        <i data-lucide="briefcase" class="w-5 h-5 text-indigo-400"></i>
                        <span>Seller Portal</span>
                    </a>'''

if mobile_btn_old in html:
    html = html.replace(mobile_btn_old, mobile_btn_new)
    print("Added Upload Product button to mobile drawer")
else:
    print("Warning: mobile_btn_old not matched")

# 3. Enhance categories dropdown in admin-sec-add-product
old_cat_select = '''<select id="add-prod-cat" required class="w-full bg-slate-950 p-2.5 rounded-lg border border-white/10 text-xs text-white">
                                    <option value="Electronics">Electronics</option>
                                    <option value="Fashion">Fashion</option>
                                    <option value="Home & Kitchen">Home & Kitchen</option>
                                    <option value="Beauty & Personal Care">Beauty & Personal Care</option>
                                    <option value="Grocery">Grocery</option>
                                    <option value="Sports & Fitness">Sports & Fitness</option>
                                    <option value="Appliances">Appliances</option>
                                </select>'''

new_cat_select = '''<select id="add-prod-cat" required class="w-full bg-slate-950 p-2.5 rounded-xl border border-white/20 text-xs text-white focus:border-amber-400 focus:ring-1 focus:ring-amber-400">
                                    <option value="Electronics">Electronics (மின்னணு சாதனங்கள் & கேஜெட்)</option>
                                    <option value="Fashion">Fashion & Apparel (ஆடை & ஃபேஷன்)</option>
                                    <option value="Home & Kitchen">Home & Kitchen (வீடு & சமையலறை)</option>
                                    <option value="Appliances">Appliances (வீட்டு உபயோக பொருட்கள்)</option>
                                    <option value="Beauty & Personal Care">Beauty & Personal Care (அழகு சாதனங்கள்)</option>
                                    <option value="Sports & Fitness">Sports & Fitness (விளையாட்டு & உடற்பயிற்சி)</option>
                                    <option value="Books & Education">Books & Education (புத்தகங்கள் & கல்வி)</option>
                                    <option value="Grocery">Grocery & Gourmet (மளிகை பொருட்கள்)</option>
                                    <option value="Toys & Baby">Toys & Baby Products (பொம்மைகள் & குழந்தைகள்)</option>
                                    <option value="Automotive">Automotive & Accessories (வாகன பாகங்கள்)</option>
                                    <option value="Health & Wellness">Health & Wellness (சுகாதாரம் & ஆரோக்கியம்)</option>
                                    <option value="Industrial & Scientific">Industrial & Scientific (தொழில்துறை உபகரணங்கள்)</option>
                                </select>'''

if old_cat_select in html:
    html = html.replace(old_cat_select, new_cat_select)
    print("Replaced category dropdown with all 12 categories")
else:
    print("Warning: old_cat_select not matched")

# 4. Enhance handleImagePreview to upload to /api/upload-image
old_img_preview_fn = '''        function handleImagePreview(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                const previewContainer = document.getElementById('image-preview-container');
                if (previewContainer) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" class="w-full h-full object-contain rounded-xl" />`;
                }
                const imgUrlInput = document.getElementById('add-prod-img-url');
                if (imgUrlInput && !imgUrlInput.value) {
                    imgUrlInput.value = e.target.result;
                }
            };
            reader.readAsDataURL(file);
        }'''

new_img_preview_fn = '''        async function handleImagePreview(event) {
            const file = event.target.files[0];
            if (!file) return;

            // Instant local preview
            const reader = new FileReader();
            reader.onload = function(e) {
                const previewContainer = document.getElementById('image-preview-container');
                if (previewContainer) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" class="w-full h-full object-contain rounded-xl" />`;
                }
            };
            reader.readAsDataURL(file);

            // Upload directly to server storage
            const formData = new FormData();
            formData.append('file', file);
            try {
                showToast('Uploading image to Next Vision Brand server...', 'info');
                const res = await fetch('/api/upload-image', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (res.ok && data.url) {
                    const imgUrlInput = document.getElementById('add-prod-img-url');
                    if (imgUrlInput) {
                        imgUrlInput.value = data.url;
                    }
                    showToast('Image uploaded successfully! (படம் பதிவேற்றப்பட்டது)', 'success');
                } else {
                    showToast('Failed to upload image to server.', 'error');
                }
            } catch (err) {
                console.error(err);
                showToast('Error uploading image to server.', 'error');
            }
        }'''

if old_img_preview_fn in html:
    html = html.replace(old_img_preview_fn, new_img_preview_fn)
    print("Replaced handleImagePreview with server uploader")
else:
    print("Warning: old_img_preview_fn not matched")

# 5. Enhance handleAdminAddProduct
idx_handler = html.find('async function handleAdminAddProduct')
idx_handler_end = html.find('async function handleBulkCSVUpload', idx_handler)
if idx_handler != -1 and idx_handler_end != -1:
    old_handler_code = html[idx_handler:idx_handler_end]
    new_handler_code = '''async function handleAdminAddProduct(e) {
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
                showToast('Please enter a valid Selling Price (சரியான விலையை உள்ளிடவும்).', 'error');
                return;
            }

            let specsObj = {};
            if (specsRaw) {
                try {
                    specsObj = JSON.parse(specsRaw);
                } catch (err) {
                    // Try key-value format if user typed "Key: Value"
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
                    // Reset form
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
        }\n\n        '''
    html = html[:idx_handler] + new_handler_code + html[idx_handler_end:]
    print("Replaced handleAdminAddProduct with robust version")
else:
    print("Warning: handleAdminAddProduct bounds not found")

# 6. Update navigate function to support #upload and #upload-product routes
old_nav_def = '''function navigate(viewName, updateHash = true) {
            viewName = (viewName || 'home').replace(/^#+/, '');'''

new_nav_def = '''function navigate(viewName, updateHash = true) {
            viewName = (viewName || 'home').replace(/^#+/, '');
            if (viewName === 'upload' || viewName === 'upload-product') {
                navigate('admin', updateHash);
                switchAdminTab('add-product');
                return;
            }'''

if old_nav_def in html:
    html = html.replace(old_nav_def, new_nav_def)
    print("Updated navigate function with #upload routes")
else:
    print("Warning: old_nav_def not matched")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("All upload improvements applied successfully!")
