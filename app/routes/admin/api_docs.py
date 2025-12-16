# API Documentation Routes with Swagger UI
"""
Swagger/OpenAPI Documentation for the School Website REST API.

Uses flask-swagger-ui for proper Swagger interface.
"""
from flask import jsonify, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes.admin import admin_bp


# Swagger UI configuration
SWAGGER_URL = '/admin/api/swagger'  # Swagger UI endpoint
API_URL = '/admin/api/spec'  # OpenAPI spec endpoint

# Create Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SMA Medina Bandung API",
        'layout': 'BaseLayout',
        'deepLinking': True,
        'displayRequestDuration': True,
        'docExpansion': 'list',
        'filter': True
    }
)


# Simple docs page that redirects to swagger
@admin_bp.route('/api/docs')
def api_docs():
    """
    Redirect to Swagger UI documentation.
    """
    from flask import redirect
    return redirect('/admin/api/swagger')


@admin_bp.route('/api/spec')
def api_spec():
    """
    Return OpenAPI/Swagger specification JSON.
    """
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "SMA Medina Bandung API",
            "description": """
REST API untuk manajemen konten website SMA Medina Bandung.

## Authentication
Semua endpoint memerlukan autentikasi (login sebagai admin via session).

## Features
- **Banner**: CRUD untuk hero banner di homepage
- **Galeri**: CRUD untuk foto galeri dengan upload gambar
- **Sambutan**: Update sambutan kepala sekolah dengan foto
            """,
            "version": "1.0.0",
            "contact": {
                "name": "Admin",
                "email": "smamedinabdg@gmail.com"
            }
        },
        "servers": [
            {"url": "/admin/api", "description": "Admin API Server"}
        ],
        "tags": [
            {"name": "Banner", "description": "Hero Banner management untuk homepage"},
            {"name": "Galeri", "description": "Photo gallery management"},
            {"name": "Profil Sekolah", "description": "School profile / sambutan management"}
        ],
        "paths": {
            "/banners": {
                "get": {
                    "tags": ["Banner"],
                    "summary": "List all banners",
                    "description": "Mendapatkan semua banner yang terdaftar",
                    "responses": {
                        "200": {
                            "description": "List of banners",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/Banner"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Banner"],
                    "summary": "Create new banner",
                    "description": "Upload gambar banner baru",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "required": ["gambar"],
                                    "properties": {
                                        "gambar": {"type": "string", "format": "binary", "description": "Banner image file (JPG, PNG, WebP)"},
                                        "judul": {"type": "string", "description": "Banner title"},
                                        "subjudul": {"type": "string", "description": "Banner subtitle"},
                                        "is_active": {"type": "boolean", "default": True, "description": "Active status"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Banner created successfully"},
                        "400": {"description": "Bad request - missing image or invalid file"}
                    }
                }
            },
            "/banners/{id}": {
                "get": {
                    "tags": ["Banner"],
                    "summary": "Get banner by ID",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "Banner ID"}
                    ],
                    "responses": {
                        "200": {"description": "Banner data"},
                        "404": {"description": "Banner not found"}
                    }
                },
                "put": {
                    "tags": ["Banner"],
                    "summary": "Update existing banner",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "gambar": {"type": "string", "format": "binary", "description": "New banner image (optional)"},
                                        "judul": {"type": "string"},
                                        "subjudul": {"type": "string"},
                                        "is_active": {"type": "boolean"},
                                        "display_order": {"type": "integer", "description": "Display order (lower = first)"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Banner updated"},
                        "404": {"description": "Banner not found"}
                    }
                },
                "delete": {
                    "tags": ["Banner"],
                    "summary": "Delete banner",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {"description": "Banner deleted"},
                        "404": {"description": "Banner not found"}
                    }
                }
            },
            "/banners/{id}/toggle": {
                "post": {
                    "tags": ["Banner"],
                    "summary": "Toggle banner active status",
                    "description": "Switch banner antara aktif dan nonaktif",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {"description": "Status toggled successfully"}
                    }
                }
            },
            "/galeri": {
                "get": {
                    "tags": ["Galeri"],
                    "summary": "List all gallery photos",
                    "responses": {
                        "200": {
                            "description": "List of photos",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/Galeri"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Galeri"],
                    "summary": "Add new gallery photo",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "required": ["foto", "judul", "tanggal"],
                                    "properties": {
                                        "foto": {"type": "string", "format": "binary", "description": "Photo file"},
                                        "judul": {"type": "string", "description": "Photo title"},
                                        "kategori": {"type": "string", "enum": ["Kegiatan", "Prestasi", "Fasilitas", "Lainnya"]},
                                        "tanggal": {"type": "string", "format": "date", "description": "Date (YYYY-MM-DD)"},
                                        "deskripsi": {"type": "string", "description": "Photo description"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Photo added"},
                        "400": {"description": "Bad request"}
                    }
                }
            },
            "/galeri/{id}": {
                "get": {
                    "tags": ["Galeri"],
                    "summary": "Get photo by ID",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {"description": "Photo data"},
                        "404": {"description": "Photo not found"}
                    }
                },
                "put": {
                    "tags": ["Galeri"],
                    "summary": "Update gallery photo",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "foto": {"type": "string", "format": "binary"},
                                        "judul": {"type": "string"},
                                        "kategori": {"type": "string"},
                                        "tanggal": {"type": "string", "format": "date"},
                                        "deskripsi": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Photo updated"}
                    }
                },
                "delete": {
                    "tags": ["Galeri"],
                    "summary": "Delete gallery photo",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {"description": "Photo deleted"}
                    }
                }
            },
            "/sambutan": {
                "get": {
                    "tags": ["Profil Sekolah"],
                    "summary": "Get principal greeting data",
                    "responses": {
                        "200": {
                            "description": "Sambutan data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Sambutan"
                                    }
                                }
                            }
                        }
                    }
                },
                "put": {
                    "tags": ["Profil Sekolah"],
                    "summary": "Update principal greeting",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "foto_kepsek": {"type": "string", "format": "binary", "description": "Foto kepala sekolah"},
                                        "nama_kepsek": {"type": "string", "description": "Nama kepala sekolah"},
                                        "konten": {"type": "string", "description": "Isi sambutan"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Sambutan updated"}
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Banner": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "judul": {"type": "string"},
                        "subjudul": {"type": "string"},
                        "image_url": {"type": "string"},
                        "is_active": {"type": "boolean"},
                        "display_order": {"type": "integer"}
                    }
                },
                "Galeri": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "judul": {"type": "string"},
                        "kategori": {"type": "string"},
                        "tanggal": {"type": "string", "format": "date"},
                        "deskripsi": {"type": "string"},
                        "image_url": {"type": "string"}
                    }
                },
                "Sambutan": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "nama_kepala_sekolah": {"type": "string"},
                                "foto_kepala_sekolah": {"type": "string"},
                                "sambutan_kepsek": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(spec)


def get_swagger_blueprint():
    """Return the swagger blueprint for registration."""
    return swaggerui_blueprint
