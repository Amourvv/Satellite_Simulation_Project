export interface GeoPoint {
  latitude_deg: number
  longitude_deg: number
  altitude_km: number
}

export interface Satellite {
  id: string
  name: string
  layer: string
  position: GeoPoint
  orbit_altitude_km: number
  inclination_deg: number
  compute_capacity_gflops: number
}

export interface GroundStation {
  id: string
  name: string
  position: GeoPoint
  min_elevation_deg: number
}

export interface LinkMetric {
  id: string
  source_id: string
  target_id: string
  distance_km: number
  elevation_deg: number
  free_space_path_loss_db: number
  capacity_mbps: number
  visible: boolean
}

export interface Scenario {
  name: string
  epoch_iso: string
  satellites: Satellite[]
  ground_stations: GroundStation[]
  links: LinkMetric[]
}

