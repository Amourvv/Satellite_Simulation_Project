from __future__ import annotations

from datetime import datetime, timezone
from math import asin, cos, degrees, log10, radians, sin, sqrt

from app.schemas import GeoPoint, GroundStation, LinkMetric, Satellite, Scenario

EARTH_RADIUS_KM = 6371.0
LIGHT_SPEED_MPS = 299_792_458


def build_demo_scenario() -> Scenario:
    ground_station = GroundStation(
        id="gs-beijing",
        name="Beijing Gateway",
        position=GeoPoint(latitude_deg=40.0, longitude_deg=116.4),
        min_elevation_deg=10.0,
    )

    satellites = [
        Satellite(
            id="leo-001",
            name="LEO-001",
            layer="LEO",
            position=GeoPoint(latitude_deg=43.0, longitude_deg=121.0, altitude_km=550.0),
            orbit_altitude_km=550.0,
            inclination_deg=53.0,
            compute_capacity_gflops=120.0,
        ),
        Satellite(
            id="leo-002",
            name="LEO-002",
            layer="LEO",
            position=GeoPoint(latitude_deg=25.0, longitude_deg=104.0, altitude_km=550.0),
            orbit_altitude_km=550.0,
            inclination_deg=53.0,
            compute_capacity_gflops=120.0,
        ),
        Satellite(
            id="geo-001",
            name="GEO-001",
            layer="GEO",
            position=GeoPoint(latitude_deg=0.0, longitude_deg=110.5, altitude_km=35786.0),
            orbit_altitude_km=35786.0,
            inclination_deg=0.0,
            compute_capacity_gflops=400.0,
        ),
    ]

    links = [
        _build_ground_link(satellite, ground_station)
        for satellite in satellites
    ]

    return Scenario(
        name="MVP LEO-GEO-ground coexistence demo",
        epoch_iso=datetime.now(timezone.utc).isoformat(),
        satellites=satellites,
        ground_stations=[ground_station],
        links=links,
    )


def _build_ground_link(satellite: Satellite, ground_station: GroundStation) -> LinkMetric:
    distance_km, elevation_deg = _range_and_elevation(
        satellite.position,
        ground_station.position,
    )
    fspl_db = _free_space_path_loss_db(distance_km=distance_km, frequency_ghz=20.0)
    capacity_mbps = _shannon_capacity_mbps(bandwidth_mhz=100.0, snr_db=max(0.0, 35.0 - fspl_db / 10.0))
    visible = elevation_deg >= ground_station.min_elevation_deg

    return LinkMetric(
        id=f"{satellite.id}-{ground_station.id}",
        source_id=satellite.id,
        target_id=ground_station.id,
        distance_km=round(distance_km, 3),
        elevation_deg=round(elevation_deg, 3),
        free_space_path_loss_db=round(fspl_db, 3),
        capacity_mbps=round(capacity_mbps, 3) if visible else 0.0,
        visible=visible,
    )


def _range_and_elevation(space_point: GeoPoint, ground_point: GeoPoint) -> tuple[float, float]:
    sx, sy, sz = _ecef_km(space_point)
    gx, gy, gz = _ecef_km(ground_point)
    rx, ry, rz = sx - gx, sy - gy, sz - gz
    distance = sqrt(rx * rx + ry * ry + rz * rz)

    lat = radians(ground_point.latitude_deg)
    lon = radians(ground_point.longitude_deg)
    ux = cos(lat) * cos(lon)
    uy = cos(lat) * sin(lon)
    uz = sin(lat)

    elevation = degrees(asin((rx * ux + ry * uy + rz * uz) / distance))
    return distance, elevation


def _ecef_km(point: GeoPoint) -> tuple[float, float, float]:
    radius = EARTH_RADIUS_KM + point.altitude_km
    lat = radians(point.latitude_deg)
    lon = radians(point.longitude_deg)
    return (
        radius * cos(lat) * cos(lon),
        radius * cos(lat) * sin(lon),
        radius * sin(lat),
    )


def _free_space_path_loss_db(distance_km: float, frequency_ghz: float) -> float:
    return 92.45 + 20.0 * log10(distance_km) + 20.0 * log10(frequency_ghz)


def _shannon_capacity_mbps(bandwidth_mhz: float, snr_db: float) -> float:
    snr_linear = 10.0 ** (snr_db / 10.0)
    capacity_bps = bandwidth_mhz * 1_000_000 * log10(1.0 + snr_linear) / log10(2.0)
    return capacity_bps / 1_000_000

