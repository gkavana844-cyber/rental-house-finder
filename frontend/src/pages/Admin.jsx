import React, { useState, useEffect } from 'react';
import '../styles/Admin.css';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [activities, setActivities] = useState([]);
  const [stats, setStats] = useState({
    totalUsers: 0,
    housesAdded: 0,
    totalSearches: 0,
    last24Hours: 0,
    activitiesByType: {}
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterType, setFilterType] = useState('all');

  const BACKEND_URL = 'https://rental-house-finder-backend.onrender.com/api';

  // Fetch activities and stats
  useEffect(() => {
    fetchData();
    // Auto-refresh every 10 seconds
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch activities
      const activitiesResponse = await fetch(`${BACKEND_URL}/activities/recent?limit=20`);
      const activitiesData = await activitiesResponse.json();
      
      // Fetch stats
      const statsResponse = await fetch(`${BACKEND_URL}/activities/stats`);
      const statsData = await statsResponse.json();

      if (activitiesData.success && statsData.success) {
        setActivities(activitiesData.data);
        setStats({
          totalUsers: statsData.data.activities_by_type.user_registered || 0,
          housesAdded: statsData.data.activities_by_type.house_added || 0,
          totalSearches: statsData.data.activities_by_type.user_searched || 0,
          last24Hours: statsData.data.last_24_hours || 0,
          activitiesByType: statsData.data.activities_by_type || {}
        });
      }
      
      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Filter activities by type
  const getFilteredActivities = () => {
    if (filterType === 'all') {
      return activities;
    }
    return activities.filter(activity => activity.type === filterType);
  };

  // Get activity count by type
  const getActivityCount = (type) => {
    return stats.activitiesByType[type] || 0;
  };

  const filteredActivities = getFilteredActivities();

  const activityTypes = [
    { key: 'user_registered', label: '👤 User Registered', color: '#3b82f6' },
    { key: 'house_added', label: '🏠 House Added', color: '#10b981' },
    { key: 'user_searched', label: '🔍 User Searched', color: '#f59e0b' },
    { key: 'furniture_selected', label: '🛋️ Furniture Selected', color: '#8b5cf6' },
    { key: 'nearby_viewed', label: '📍 Nearby Viewed', color: '#ec4899' }
  ];

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>👨‍💼 Admin Panel</h1>
        <div className="refresh-btn" onClick={fetchData} disabled={loading}>
          {loading ? '⏳ Loading...' : '🔄 Refresh'}
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {/* Tabs Navigation */}
      <div className="tabs-navigation">
        <button
          className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          className={`tab-btn ${activeTab === 'activities' ? 'active' : ''}`}
          onClick={() => setActiveTab('activities')}
        >
          📋 Activities
        </button>
        <button
          className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📈 Analytics
        </button>
      </div>

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && (
        <div className="tab-content dashboard-tab">
          {/* Main Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card primary">
              <div className="stat-icon">👤</div>
              <div className="stat-content">
                <div className="stat-number">{stats.totalUsers}</div>
                <div className="stat-label">Total Users</div>
              </div>
            </div>

            <div className="stat-card success">
              <div className="stat-icon">🏠</div>
              <div className="stat-content">
                <div className="stat-number">{stats.housesAdded}</div>
                <div className="stat-label">Houses Added</div>
              </div>
            </div>

            <div className="stat-card warning">
              <div className="stat-icon">🔍</div>
              <div className="stat-content">
                <div className="stat-number">{stats.totalSearches}</div>
                <div className="stat-label">Total Searches</div>
              </div>
            </div>

            <div className="stat-card info">
              <div className="stat-icon">⚡</div>
              <div className="stat-content">
                <div className="stat-number">{stats.last24Hours}</div>
                <div className="stat-label">Last 24 Hours</div>
              </div>
            </div>
          </div>

          {/* Activity Type Breakdown */}
          <div className="activity-breakdown">
            <h2>📊 Activity Breakdown</h2>
            <div className="breakdown-grid">
              {activityTypes.map(type => (
                <div key={type.key} className="breakdown-card">
                  <div className="breakdown-icon">{type.label.split(' ')[0]}</div>
                  <div className="breakdown-content">
                    <div className="breakdown-label">{type.label}</div>
                    <div className="breakdown-count">{getActivityCount(type.key)}</div>
                  </div>
                  <div 
                    className="breakdown-bar"
                    style={{
                      width: `${(getActivityCount(type.key) / Math.max(stats.totalUsers, stats.housesAdded, stats.totalSearches, 1)) * 100}%`,
                      backgroundColor: type.color
                    }}
                  ></div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activities */}
          <div className="recent-activities">
            <h2>📋 Recent Activities</h2>
            {loading ? (
              <p className="loading">Loading activities...</p>
            ) : activities.length === 0 ? (
              <p className="no-data">No activities yet</p>
            ) : (
              <div className="activities-list">
                {activities.slice(0, 5).map(activity => (
                  <div key={activity.id} className="activity-item">
                    <div className="activity-icon">{activity.icon}</div>
                    <div className="activity-info">
                      <div className="activity-desc">{activity.description}</div>
                      <div className="activity-time">
                        {new Date(activity.timestamp).toLocaleString()}
                      </div>
                    </div>
                    <div className="activity-type">{activity.type}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Activities Tab */}
      {activeTab === 'activities' && (
        <div className="tab-content activities-tab">
          <div className="activities-header">
            <h2>📋 All Activities</h2>
            <div className="filter-controls">
              <select 
                className="filter-select"
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
              >
                <option value="all">All Activities</option>
                <option value="user_registered">👤 User Registered</option>
                <option value="house_added">🏠 House Added</option>
                <option value="user_searched">🔍 User Searched</option>
                <option value="furniture_selected">🛋️ Furniture Selected</option>
                <option value="nearby_viewed">📍 Nearby Viewed</option>
              </select>
            </div>
          </div>

          {loading ? (
            <p className="loading">Loading activities...</p>
          ) : filteredActivities.length === 0 ? (
            <p className="no-data">No activities found</p>
          ) : (
            <div className="activities-table-container">
              <table className="activities-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Description</th>
                    <th>User ID</th>
                    <th>Timestamp</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredActivities.map(activity => (
                    <tr key={activity.id} className="activity-row">
                      <td className="type-cell">
                        <span className="type-badge">
                          {activity.icon} {activity.type}
                        </span>
                      </td>
                      <td className="desc-cell">{activity.description}</td>
                      <td className="user-cell">{activity.userId || 'N/A'}</td>
                      <td className="time-cell">
                        {new Date(activity.timestamp).toLocaleString()}
                      </td>
                      <td className="details-cell">
                        {activity.metadata ? (
                          <button 
                            className="details-btn"
                            onClick={() => {
                              alert(JSON.stringify(activity.metadata, null, 2));
                            }}
                          >
                            View
                          </button>
                        ) : (
                          'N/A'
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="activities-footer">
            <p>Showing {filteredActivities.length} of {activities.length} activities</p>
          </div>
        </div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <div className="tab-content analytics-tab">
          <h2>📈 Analytics & Insights</h2>

          <div className="analytics-grid">
            {/* Activity Distribution */}
            <div className="analytics-card">
              <h3>🎯 Activity Distribution</h3>
              <div className="distribution-chart">
                {activityTypes.map(type => {
                  const count = getActivityCount(type.key);
                  const percentage = stats.totalSearches > 0 
                    ? Math.round((count / stats.totalSearches) * 100)
                    : 0;
                  
                  return (
                    <div key={type.key} className="distribution-item">
                      <div className="distribution-label">
                        <span>{type.label}</span>
                        <span className="count">{count}</span>
                      </div>
                      <div className="distribution-bar">
                        <div 
                          className="distribution-fill"
                          style={{
                            width: `${percentage}%`,
                            backgroundColor: type.color
                          }}
                        ></div>
                      </div>
                      <div className="distribution-percent">{percentage}%</div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Summary Stats */}
            <div className="analytics-card">
              <h3>📊 Summary Stats</h3>
              <div className="summary-stats">
                <div className="summary-item">
                  <span className="summary-label">Total Activities:</span>
                  <span className="summary-value">{stats.totalSearches}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Last 24 Hours:</span>
                  <span className="summary-value">{stats.last24Hours}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Avg per Hour:</span>
                  <span className="summary-value">
                    {stats.last24Hours > 0 ? (stats.last24Hours / 24).toFixed(1) : 0}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">User Engagement:</span>
                  <span className="summary-value">
                    {stats.totalUsers > 0 ? ((stats.totalSearches / stats.totalUsers) * 100).toFixed(1) : 0}%
                  </span>
                </div>
              </div>
            </div>

            {/* Top Activities */}
            <div className="analytics-card full-width">
              <h3>🔝 Top Activities</h3>
              <div className="top-activities">
                {activityTypes
                  .map(type => ({
                    ...type,
                    count: getActivityCount(type.key)
                  }))
                  .sort((a, b) => b.count - a.count)
                  .slice(0, 5)
                  .map((type, index) => (
                    <div key={type.key} className="top-item">
                      <div className="rank">#{index + 1}</div>
                      <div className="top-label">{type.label}</div>
                      <div className="top-count">{type.count}</div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Admin;