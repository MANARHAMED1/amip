import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000/api")
TIMEOUT = 15


def _get_auth_headers():
    token = st.session_state.get("jwt_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def get(endpoint: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=TIMEOUT,
                         headers=_get_auth_headers())
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("API unreachable - verify backend is running on port 8000")
        return None
    except requests.exceptions.Timeout:
        st.error("API timeout - server took too long to respond")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.session_state.authenticated = False
            st.session_state.jwt_token = None
            st.rerun()
        st.error(f"API error {e.response.status_code}: {e.response.text[:200]}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


def get_with_filters(endpoint: str, extra_params: dict | None = None):
    params = {}
    ds = st.session_state.get("date_start")
    de = st.session_state.get("date_end")
    if ds and de:
        params["date_start"] = ds.isoformat()
        params["date_end"] = de.isoformat()
    sector = st.session_state.get("sector_filter")
    if sector and sector != "Tous":
        params["sector"] = sector
    machine = st.session_state.get("machine_filter")
    if machine and machine != "Toutes":
        params["machine"] = machine
    if extra_params:
        params.update(extra_params)
    return get(endpoint, params=params if params else None)
