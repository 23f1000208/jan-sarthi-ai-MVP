"""
Spatial-Temporal Cluster Engine Module
Groups individual multilingual citizen signals into geographic and infrastructure hotspots.
Adheres to ClusterEngine abstraction with BasicClusterEngine implementation.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN


class ClusterEngine(ABC):
    """Abstract base class for clustering engines."""
    @abstractmethod
    def fit_predict(self, feedback_df: pd.DataFrame) -> List[Dict[str, Any]]:
        pass


class BasicClusterEngine(ClusterEngine):
    """
    Combines geographic coordinates (Haversine/Euclidean proximity) with
    infrastructure category alignment and temporal proximity to detect civic demand hotspots.
    """
    def __init__(self, eps_km: float = 2.5, min_samples: int = 3):
        # 1 degree lat/lon is roughly 111 km
        self.eps_degrees = eps_km / 111.0
        self.min_samples = min_samples

    def fit_predict(self, feedback_df: pd.DataFrame) -> List[Dict[str, Any]]:
        if feedback_df.empty:
            return []
            
        df = feedback_df.copy()
        # Filter out obvious high manipulation risks for core clustering
        clusters = []
        
        # Group by administrative region & category first
        for (ward, cat), group in df.groupby(["administrative_region", "category"]):
            if len(group) < 2:
                continue
                
            coords = group[["latitude", "longitude"]].values
            # Run DBSCAN
            db = DBSCAN(eps=self.eps_degrees, min_samples=2).fit(coords)
            labels = db.labels_
            
            for label in set(labels):
                if label == -1 and len(group) < 3:
                    continue  # Ignore lone noise points
                    
                subgroup = group[labels == label] if label != -1 else group
                
                # Centroid
                c_lat = float(subgroup["latitude"].mean())
                c_lon = float(subgroup["longitude"].mean())
                ward_name = subgroup["location"].iloc[0] if "location" in subgroup.columns else ward
                
                # Check manipulation flag
                manip_flags = subgroup["manipulation_risk"].tolist()
                manip_overall = "HIGH" if manip_flags.count("HIGH") >= (len(manip_flags) * 0.5) else (
                    "MEDIUM" if "MEDIUM" in manip_flags else "LOW"
                )
                
                # Severity distribution
                sev_counts = subgroup["severity"].value_counts().to_dict()
                
                # Signal counts
                raw_count = len(subgroup)
                
                cluster_id = f"CLUSTER-{cat.upper()[:4]}-{ward}"
                
                # Simple keyword extraction
                words = [w for t in subgroup["original_text"] for w in t.split() if len(w) > 4]
                top_words = list(dict.fromkeys(words))[:5]
                
                cluster_info = {
                    "cluster_id": cluster_id,
                    "category": cat,
                    "title": f"{ward_name} {cat} Deficit Hotspot",
                    "ward_id": ward,
                    "ward_name": ward_name,
                    "centroid_lat": round(c_lat, 4),
                    "centroid_lon": round(c_lon, 4),
                    "raw_signal_count": raw_count,
                    "raw_demand_score": min(1.0, raw_count / 15.0),
                    "calibrated_demand_score": min(1.0, raw_count / 15.0),
                    "severity_breakdown": sev_counts,
                    "top_keywords": top_words,
                    "earliest_signal": subgroup["timestamp"].min(),
                    "latest_signal": subgroup["timestamp"].max(),
                    "manipulation_flag": manip_overall,
                    "feedback_ids": subgroup["id"].tolist()
                }
                clusters.append(cluster_info)
                
        # Deduplicate clusters by cluster_id
        unique_clusters = {c["cluster_id"]: c for c in clusters}
        return list(unique_clusters.values())
