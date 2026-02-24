import os

content = """{% extends 'layouts/base_admin.html' %}
{% block title %}Enviados{% endblock %}
{% block page_title %}Documentos Enviados{% endblock %}
{% block content %}
<div class="premium-card mb-4">
    <div class="card-p-header">
        <h6 class="m-0"><i class="bi bi-funnel-fill me-2 text-primary"></i> Filtrar Salida</h6>
    </div>
    <div class="card-p-body">
        <form method="get" class="row g-3">
            <div class="col-md-5">
                <label class="form-label-premium">Búsqueda rápida</label>
                <div class="input-group-premium">
                    <i class="bi bi-search"></i>
                    <input type="text" name="q" placeholder="Proveedor o Tipo..." value="{{ q_actual }}">
                </div>
            </div>
            <div class="col-md-5">
                <label class="form-label-premium">Categoría</label>
                <select name="tipo" class="premium-select">
                    <option value="">Todas las Categorías</option>
                    {% for t in categorias %}
                    <option value="{{ t.id }}" {% if tipo_actual == t.id|stringformat:"s" %}selected{% endif %}>{{ t.nombre }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="submit" class="btn-premium-blue w-100 py-2">
                    Aplicar
                </button>
            </div>
        </form>
    </div>
</div>

<div class="premium-card">
    <div class="card-p-body p-0">
        <div class="table-responsive">
            <table class="table premium-table align-middle m-0">
                <thead>
                    <tr>
                        <th class="ps-4">Destinatario</th>
                        <th>Documento</th>
                        <th>Fecha Envío</th>
                        <th>Vencimiento</th>
                        <th class="text-center">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for doc in documentos %}
                    <tr>
                        <td class="ps-4">
                            <div class="provider-info">
                                <span class="provider-name">{{ doc.proveedor.nombre }}</span>
                                <span class="provider-nit">{{ doc.proveedor.nit }}</span>
                            </div>
                        </td>
                        <td>
                            <div class="doc-type-info">
                                <span class="doc-badge">{{ doc.tipo_documento.nombre }}</span>
                                {% if doc.descripcion %}
                                <div class="doc-desc" title="{{ doc.descripcion }}">{{ doc.descripcion|truncatechars:45 }}</div>
                                {% endif %}
                            </div>
                        </td>
                        <td>
                            <div class="text-slate-600 small">
                                <i class="bi bi-calendar3 me-1"></i> {{ doc.fecha_carga|date:"d/m/Y" }}
                                <span class="text-muted ms-1">{{ doc.fecha_carga|date:"H:i" }}</span>
                            </div>
                        </td>
                        <td>
                            {% if doc.fecha_vencimiento %}
                            {% if doc.esta_vencido %}
                            <span class="text-danger fw-bold small"><i class="bi bi-exclamation-circle"></i> {{ doc.fecha_vencimiento|date:"d/m/Y" }}</span>
                            {% else %}
                            <span class="text-success small fw-bold">{{ doc.fecha_vencimiento|date:"d/m/Y" }}</span>
                            {% endif %}
                            {% else %}
                            <span class="text-muted small">Sin vencimiento</span>
                            {% endif %}
                        </td>
                        <td class="text-center">
                            <div class="acciones-botones">
                                <button type="button" onclick="openPdfViewer('{% url 'serve_document_pdf' doc.pk %}')"
                                    class="btn-action view" title="Visualizar">
                                    <i class="bi bi-eye-fill"></i> <span class="ms-1">Ver</span>
                                </button>
                                <a href="{{ doc.archivo.url }}" target="_blank" class="btn-action view" title="Ver PDF">
                                    <i class="bi bi-file-earmark-pdf-fill"></i> <span class="ms-1">PDF</span>
                                </a>
                            </div>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center py-5">
                            <div class="empty-table-state">
                                <i class="bi bi-send-x text-muted opacity-25" style="font-size: 3rem;"></i>
                                <p class="text-muted mt-2">No se han enviado documentos todavía.</p>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

<style>
    /* Reuse global styles or define specific ones here */
    .form-label-premium { font-size: 0.65rem; font-weight: 700; color: #475569; margin-bottom: 4px; display: block; text-transform: uppercase; }
    .input-group-premium { position: relative; display: flex; align-items: center; }
    .input-group-premium i { position: absolute; left: 10px; color: #94a3b8; font-size: 0.8rem; }
    .input-group-premium input { width: 100%; padding: 6px 10px 6px 32px; border: 1.5px solid #e2e8f0; border-radius: 6px; font-size: 0.85rem; background: #f8fafc; }
    .premium-select { width: 100%; padding: 6px 10px; border: 1.5px solid #e2e8f0; border-radius: 6px; font-size: 0.85rem; background: #f8fafc; }
    .premium-card { background: #fff; border-radius: 12px; border: 1px solid #f1f5f9; box-shadow: 0 2px 4px rgba(0,0,0,0.05); overflow: hidden; }
    .card-p-header { padding: 10px 16px; border-bottom: 1px solid #f1f5f9; }
    .card-p-body { padding: 12px 16px; }
    .premium-table thead th { background: #f8fafc; padding: 8px 16px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; color: #64748b; }
    .premium-table tbody td { padding: 10px 16px; }
    .provider-info { display: flex; flex-direction: column; }
    .provider-name { font-weight: 700; color: #1e293b; font-size: 0.85rem; }
    .provider-nit { color: #64748b; font-size: 0.7rem; }
    .doc-badge { font-weight: 600; color: #1e40af; font-size: 0.8rem; }
    .doc-desc { font-size: 0.7rem; color: #94a3b8; font-style: italic; }
    .btn-action { padding: 5px 12px; display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; transition: all 0.2s; border: 1px solid transparent; background: #f1f5f9; color: #64748b; text-decoration: none !important; font-size: 0.75rem; font-weight: 600; }
    .btn-action.view { background: #eff6ff; color: #2563eb; border-color: #dbeafe; }
    .btn-action.view:hover { background: #2563eb; color: #fff; border-color: #1e40af; }
    .btn-premium-blue { background: linear-gradient(135deg, #2563eb, #1e40af); color: #fff; border: none; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }
    
    .acciones-botones {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
</style>
{% endblock %}"""

path = r'proveedores\templates\proveedores\admin\document_outbox.html'
abs_path = os.path.abspath(path)
print(f"Borrando y escribiendo: {abs_path}")
if os.path.exists(abs_path):
    os.remove(abs_path)
with open(abs_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)
    f.flush()
    os.fsync(f.fileno())
print(f"Escritura completada para {abs_path}")
