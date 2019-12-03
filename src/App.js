import React from 'react';
import './App.css';
import Spell from './components/Spell';

import attackJSON from './json/attack';
import defenseJSON from './json/defense';
import iconJSON from './json/icon';
// import warpsJSON from './json/warps';
// import weirdnessJSON from './json/weirdness';

export default class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentCategory: '',
			currentIcon: '',
			warpAttack: false,
			warpDefense: false,
			warpIcon: false,
			addNecromancy: false,
			addWizardry: false,
			addDivine: false,
			addSorcery: false,
			spellLevel: '1'
		};
		this.state.arrSpells = this.getSpellArray();
		this.state.arrIcons = Object.keys(iconJSON);

		this.handleInputChange = this.handleInputChange.bind(this);
	}

	getSpellArray() {
		let spells = ['a', 'a', 'd', 'd', 'i', 'i'];
		for (let i in spells) {
			let r = Math.floor(Math.random() * spells.length);
			[spells[i], spells[r]] = [spells[r], spells[i]];
		}
		return spells;
	}

	handleInputChange(event) {
		const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
		this.setState({[event.target.name]: value});
	}

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

		console.log(this.getSpellArray());

		return (
			<div key="container" className="container-fluid">

				<div className="row bg-primary">

				<div className="col-12 border-bottom"><h1 className="text-center text-light">Chaos Mage</h1></div>

				<div className="col-12"><ul className="nav nav-fill text-light">
					<li className="nav-item">
						<button className="btn btn-warning btn-lg mt-5">Random Spell</button>
					</li>
					<li className="nav-item text-left border-left pl-1">
						<div className="form-check">
							<input className="form-check-input" type="checkbox" name="warpAttack"
								checked={this.state.warpAttack} onChange={this.handleInputChange}/>
							<label className="form-check-label">Attacking Warp</label>
						</div>
						<div className="form-check">
						<input className="form-check-input" type="checkbox" name="warpDefense"
							checked={this.state.warpDefense} onChange={this.handleInputChange}/>
							<label className="form-check-label">Defensive Warp</label>
						</div>
						<div className="form-check">
						<input className="form-check-input" type="checkbox" name="warpIcon"
							checked={this.state.warpIcon} onChange={this.handleInputChange}/>
							<label className="form-check-label">Iconic Warp</label>
						</div>
						<button className="btn btn-info btn-sm mt-2">Trigger High Weirdness</button>
					</li>
					<li className="nav-item text-left border-left pl-1">
						<div className="form-check">
							<input className="form-check-input" type="checkbox" name="addNecromancy"
								checked={this.state.addNecromancy} onChange={this.handleInputChange} />
							<label className="form-check-label">Stench of Necromancy</label>
						</div>
						<div className="form-check">
							<input className="form-check-input" type="checkbox" name="addWizardry"
								checked={this.state.addWizardry} onChange={this.handleInputChange} />
							<label className="form-check-label">Touch of Wizardry</label>
						</div>
						<div className="form-check">
							<input className="form-check-input" type="checkbox" name="addDivine"
								checked={this.state.addDivine} onChange={this.handleInputChange} />
							<label className="form-check-label">Trace of the Divine</label>
						</div>
						<div className="form-check">
							<input className="form-check-input" type="checkbox" name="addSorcery"
								checked={this.state.addSorcery} onChange={this.handleInputChange} />
							<label className="form-check-label">Whiff of Sorcery</label>
						</div>
						<div className="input-group input-group-sm my-1">
							<div className="input-group-prepend">
								<span className="input-group-text">Level</span>
							</div>
							<select className="custom-select" name="spellLevel" value={this.state.spellLevel} onChange={this.handleInputChange}>
								<option value="1">1</option>
								<option value="3">3</option>
								<option value="5">5</option>
								<option value="7">7</option>
								<option value="9">9</option>
							</select>
							<div className="input-group-append">
								<button className="btn btn-success">New Daily Spell(s)</button>
							</div>
						</div>
					</li>
				</ul></div>
				</div>

			</div>
		);
	}
}
