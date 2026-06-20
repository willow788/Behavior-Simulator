import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Page configuration
st.set_page_config(page_title="Human Behavior Simulator", layout="wide", initial_sidebar_state="expanded")

# Title with styling
st.markdown("# 🧠 Human Behavior Simulator")
st.markdown("*Visualizing stress dynamics in agent networks*")

# Create sidebar for controls
st.sidebar.markdown("### ⚙️ Simulation Parameters")
stress_spread_rate = st.sidebar.slider("🔴 Stress Spread Rate", 0.0, 1.0, 0.5, 
                                        help="How quickly stress spreads between agents (higher = faster spreading)")
recovery_rate = st.sidebar.slider("💚 Recovery Rate", 0.0, 0.1, 0.003, step=0.001,
                                   help="How quickly agents recover from stress (lower = slower recovery = more wave patterns)")
steps = st.sidebar.slider("⏱️ Simulation Steps", 10, 2500, 2500,
                           help="Number of simulation iterations to run")

#setting the grid size
N = 20

# Initialize session state for persistent simulation
if 'stress' not in st.session_state:
    st.session_state.stress = np.random.rand(N, N) * 0.1  # Start with very low stress
    st.session_state.energy = np.ones((N, N))
    st.session_state.resilience = np.random.rand(N, N)
    st.session_state.influence = np.random.rand(N, N)
    st.session_state.stress_history = []
    
    # Create connections
    st.session_state.connections = {}
    for i in range(N):
        for j in range(N):
            neighbours = []
            for _ in range(3):
                x = np.random.randint(0, N)
                y = np.random.randint(0, N)
                neighbours.append((x, y))
            st.session_state.connections[(i, j)] = neighbours

stress = st.session_state.stress
energy = st.session_state.energy
resilience = st.session_state.resilience
influence = st.session_state.influence
connections = st.session_state.connections
stress_history = st.session_state.stress_history


# Simulation update function
def update_simulation(frame):
    global stress, energy
    
    new_stress = stress.copy()
    
    if frame % 30 == 0 and frame > 50:  # Delay first stress event to see initial state
        x, y = np.random.randint(0, N, 2)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x+dx < N and 0 <= y+dy < N:
                    stress[x+dx][y+dy] += 0.8
    
    if frame == 200:  # Delay global stress increase
        stress += 0.4
    
    if frame % 20 == 0:
        stress -= 0.03
    
    # Neighbor influence and recovery
    for i in range(N):
        for j in range(N):
            neighbours = [stress[x][y] for (x, y) in connections[(i, j)]]
            
            for n in neighbours:
                if n > 0.7:
                    new_stress[i][j] += stress_spread_rate * n * influence[i][j]
                
                new_stress[i][j] -= recovery_rate * energy[i][j] * resilience[i][j]
    
    stress = np.clip(new_stress, 0, 1)
    energy = np.clip(energy + 0.01 - stress * 0.02, 0, 1)
    stress_history.append(np.mean(stress))
    
    return stress, energy

# Run simulation
st.sidebar.markdown("---")
if st.sidebar.button("🚀 Run Simulation", key="run_btn"):
    st.session_state.run_sim = True

if st.session_state.get('run_sim', False):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create container for live heatmap display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Live Stress Distribution")
        heatmap_placeholder = st.empty()
    
    with col2:
        st.markdown("### 📈 Real-time Statistics")
        stats_placeholder = st.empty()
    
    # Store frame snapshots for progression view
    frame_snapshots = []
    snapshot_interval = max(1, steps // 10)  # Capture ~10 key frames for progression
    
    for frame in range(steps):
        stress, energy = update_simulation(frame)
        st.session_state.stress = stress
        st.session_state.energy = energy
        st.session_state.stress_history = stress_history
        
        # Capture snapshots at regular intervals
        if frame % snapshot_interval == 0 or frame == steps - 1:
            frame_snapshots.append(stress.copy())
        
        progress = (frame + 1) / steps
        progress_bar.progress(progress)
        status_text.text(f"Simulation Progress: {int(progress * 100)}%")
        
        # Update live heatmap only every 100 frames for speed
        if frame % 10 == 0 or frame == steps - 1:
            with heatmap_placeholder.container():
                fig, ax = plt.subplots(figsize=(7, 6))
                mat = ax.matshow(stress, cmap='plasma', vmin=0, vmax=1)
                ax.set_title(f"Frame {frame + 1}/{steps} - Agent Stress Levels", fontsize=11, fontweight='bold')
                plt.colorbar(mat, label='Stress Level', ax=ax)
                st.pyplot(fig)
                plt.close(fig)
            
            with stats_placeholder.container():
                avg_stress = np.mean(stress)
                max_stress = np.max(stress)
                min_stress = np.min(stress)
                st.metric("Average Stress", f"{avg_stress:.3f}")
                st.metric("Maximum Stress", f"{max_stress:.3f}")
                st.metric("Minimum Stress", f"{min_stress:.3f}")
    
    status_text.success("✅ Simulation Complete!")
    
    # Display progression comparison
    st.markdown("---")
    st.markdown("### 🎬 Simulation Progression (Key Frames)")
    
    if frame_snapshots:
        # Display snapshots in rows of 3 for better visualization
        for row_idx in range(0, len(frame_snapshots), 3):
            progress_cols = st.columns(min(3, len(frame_snapshots) - row_idx))
            for col_idx, col in enumerate(progress_cols):
                frame_idx = row_idx + col_idx
                if frame_idx < len(frame_snapshots):
                    frame_stress = frame_snapshots[frame_idx]
                    with col:
                        fig, ax = plt.subplots(figsize=(5, 4))
                        mat = ax.matshow(frame_stress, cmap='plasma', vmin=0, vmax=1)
                        progress_pct = int((frame_idx / (len(frame_snapshots) - 1)) * 100) if len(frame_snapshots) > 1 else 100
                        ax.set_title(f"{progress_pct}% Progress", fontsize=10, fontweight='bold')
                        ax.set_xticks([])
                        ax.set_yticks([])
                        plt.colorbar(mat, label='Stress', ax=ax, fraction=0.046, pad=0.04)
                        st.pyplot(fig)
                        plt.close(fig)

# Plot stress trends
if stress_history:
    st.markdown("### 📉 Stress History Over Time")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(stress_history, linewidth=2, color='#FF6B6B')
    ax.fill_between(range(len(stress_history)), stress_history, alpha=0.3, color='#FF6B6B')
    ax.set_title('Average Stress History Over Time', fontsize=12, fontweight='bold')
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Average Stress Level')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

# Reset button
if st.sidebar.button("🔄 Reset Simulation"):
    st.session_state.clear()
    st.rerun()






