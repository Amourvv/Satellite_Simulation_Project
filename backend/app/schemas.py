from pydantic import BaseModel, Field


class GeoPoint(BaseModel):
    latitude_deg: float
    longitude_deg: float
    altitude_km: float = 0.0


class Satellite(BaseModel):
    id: str
    name: str
    layer: str = Field(description="Network layer, for example LEO or GEO.")
    position: GeoPoint
    orbit_altitude_km: float
    inclination_deg: float
    compute_capacity_gflops: float


class GroundStation(BaseModel):
    id: str
    name: str
    position: GeoPoint
    min_elevation_deg: float


class LinkMetric(BaseModel):
    id: str
    source_id: str
    target_id: str
    distance_km: float
    elevation_deg: float
    free_space_path_loss_db: float
    capacity_mbps: float
    visible: bool


class Scenario(BaseModel):
    name: str
    epoch_iso: str
    satellites: list[Satellite]
    ground_stations: list[GroundStation]
    links: list[LinkMetric]

