import { scriptures } from "../data/scriptures";

function Sidebar({ scripture, setScripture, section, setSection }) {
  return (
    <div className="sidebar">
      <h3> Scriptures</h3>

      <select value={scripture} onChange={(e)=>setScripture(e.target.value)}>
        {Object.keys(scriptures).map(s => <option key={s}>{s}</option>)}
      </select>

      <h3> Sections</h3>

      <div className="section-list">
        {scriptures[scripture].map(sec => (
          <div
            key={sec}
            className={section === sec ? "active" : ""}
            onClick={()=>setSection(sec)}
          >
            {sec}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Sidebar;