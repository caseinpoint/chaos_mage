import React from 'react';
// import './App.css';
import Spell from './components/Spell';

import attackJSON from './json/attack';
import defenseJSON from './json/defense';
import iconJSON from './json/icon';
// import warpsJSON from './json/warps';
// import weirdnessJSON from './json/weirdness';

export default class App extends React.Component {
	// constructor(props) {
	// 	super(props);
	// 	this.state = {};
	// }

	render() {
		let attackSpells = attackJSON.map(spell => <Spell key={spell.title} category="attack" data={spell} />);

		let defenseSpells = defenseJSON.map(spell => <Spell key={spell.title} category="defense" data={spell} />);

		let iconSpells = [];
		for (let icon in iconJSON) {
			iconSpells.push(
				<div key={icon}>
					<h2>{icon} <span className="h3 font-italic">({iconJSON[icon].feat})</span></h2>
					<div className="row">{
						iconJSON[icon].spells.map(spell => <Spell key={spell.title} category="icon" data={spell} />)
					}</div>
				</div>
			);
		}

		return (
			<div className="container-fluid">
				<h1>Attack Spells</h1>
				<div className="row">
					{attackSpells}
				</div>
				<h1>Defense Spells</h1>
				<div className="row">
					{defenseSpells}
				</div>
				<h1>Icon Spells</h1>
				{iconSpells}
			</div>
		);
	}
}
