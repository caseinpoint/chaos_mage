import React from 'react';
import './App.css';
import Spell from './components/Spell';

import attackJSON from './json/attack';
import defenseJSON from './json/defense';
import iconJSON from './json/icon';
import warpsJSON from './json/warps';
import weirdnessJSON from './json/weirdness';
import clericJSON from './json/cleric';

export default class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentCategory: '', currentIcon: '', currentWarp: undefined, currentWeird: undefined,
			warpAttack: false, warpDefense: false, warpIcon: false,
			warpText: '', warpWeird: false, // warpWeird = High Weirdness adventurer feat
			addNecromancy: false, addWizardry: false, addDivine: false, addSorcery: false,
			spellLevel: '1'
		};
		this.state.arrCategories = this.getSpellArray();
		this.state.arrIcons = Object.keys(iconJSON);

		this.handleInputChange = this.handleInputChange.bind(this);
		this.handleRandom = this.handleRandom.bind(this);
		this.handleWeirdness = this.handleWeirdness.bind(this);
		this.handleDaily = this.handleDaily.bind(this);
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

	handleWeirdness() {
		const currentWeird = weirdnessJSON.table[Math.floor(Math.random() * weirdnessJSON.table.length)]
		this.setState({ currentWeird });
	}

	handleRandom() {
		let arrCategories = this.state.arrCategories.map(x => x);
		let currentCategory = arrCategories.pop();

		if (currentCategory !== 'i') var currentIcon = '';
		else currentIcon = this.state.arrIcons[Math.floor(Math.random() * this.state.arrIcons.length)]

		if (arrCategories.length === 1) arrCategories = this.getSpellArray();

		var warpText = '';
		if (currentCategory === 'a' && this.state.warpAttack === true) {
			var currentWarp = 'attack';
			warpText = warpsJSON[currentWarp].options[Math.floor(Math.random() * warpsJSON[currentWarp].options.length)];
			if (this.state.warpWeird === true) this.handleWeirdness();
		} else if (currentCategory === 'd' && this.state.warpDefense === true) {
			currentWarp = 'defense';
			warpText = warpsJSON[currentWarp].options[Math.floor(Math.random() * warpsJSON[currentWarp].options.length)];
			if (this.state.warpWeird === true) this.handleWeirdness();
		} else if (currentCategory === 'i' && this.state.warpIcon === true) {
			currentWarp = 'icon';
			warpText = warpsJSON[currentWarp].options[Math.floor(Math.random() * warpsJSON[currentWarp].options.length)];
			if (this.state.warpWeird === true) this.handleWeirdness();
		}

		this.setState({ arrCategories, currentCategory, currentIcon, currentWarp, warpText });

		if (currentCategory === 'i' && this.state.warpWeird &&
			!this.state.warpAttack && !this.state.warpDefense && !this.state.warpIcon) {
			// High Weirdness should trigger on icon spells if adventurer feat and no warp talents
			this.handleWeirdness();
		}
	}

	handleDaily() {
		// clear old spell(s):
		let i = attackJSON.length - 1;
		while (attackJSON[i].charClass !== undefined) {
			attackJSON.pop(); i--;
		}
		i = defenseJSON.length - 1;
		while (defenseJSON[i].charClass !== undefined) {
			defenseJSON.pop(); i--;
		}

		// add new spell(s):
		if (this.state.addDivine === true) {
			const r = Math.floor(Math.random() * clericJSON[this.state.spellLevel].length);
			const spell = clericJSON[this.state.spellLevel][r];
			console.log(spell);
			if (spell.category === 'a') attackJSON.push(spell);
			else defenseJSON.push(spell);
		}
		// TODO: finish the 3 other spellcaster class JSONs and copy the above if for each one
	}

	render() {
		if (this.state.currentCategory === 'a') {
			var spells = (
				<div key="attack">
					<h2>Attack Spells:</h2>
					<div className="row px-1">
						{attackJSON.map(spell => <Spell key={spell.title} category="attack" data={spell} />)}
					</div>
				</div>
			);
		} else if (this.state.currentCategory === 'd') {
			spells = (
				<div key="defense">
					<h2>Defense Spells:</h2>
					<div className="row px-1">
						{defenseJSON.map(spell => <Spell key={spell.title} category="defense" data={spell} />)}
					</div>
				</div>
			);
		} else if (this.state.currentCategory === 'i') {
			const icon = this.state.currentIcon;
			spells = (
				<div key={icon}>
					<h2>Icon Spells: {icon} <span className="h3 font-italic">({iconJSON[icon].feat})</span></h2>
					<div className="row px-1">{
						iconJSON[icon].spells.map(spell => <Spell key={spell.title} category="icon" data={spell} />)
					}</div>
				</div>
			);
		}

		if (this.state.currentWarp !== undefined) {
			const wObj = warpsJSON[this.state.currentWarp];
			const opt = this.state.warpText;
			var warp = (
				<div key="warp">
					<p>{opt}</p>
					<p className="bg_feat text_small"><strong>Adventurer Feat:</strong> {wObj.feats.adventurer}</p>
					<p className="bg_feat text_small"><strong>Champion Feat:</strong> {wObj.feats.champion}</p>
					<p className="bg_feat text_small"><strong>Epic Feat:</strong> {wObj.feats.epic}</p>
				</div>
			);
		}

		// TODO: make the nav its own component
		return (
			<div key="container" className="container-fluid">

				<div className="row bg-primary">
					<div className="col-12 border-bottom"><h1 className="text-center text-light">Chaos Mage</h1></div>

					<div className="col-12"><ul className="nav nav-fill text-light">
						<li className="nav-item border-bottom">
							<button className="btn btn-warning btn-lg my-5" onClick={this.handleRandom}>Next Spell Category</button>
						</li>
						<li className="nav-item text-left border-left border-right border-bottom pl-1">
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
							<button className="btn btn-info btn-sm mt-1" onClick={this.handleWeirdness}>Trigger High Weirdness</button>
							<div className="form-check form-control-sm">
								<input className="form-check-input" type="checkbox" name="warpWeird"
									checked={this.state.warpWeird} onChange={this.handleInputChange}/>
								<label className="form-check-label text-white-50">Weirdness adventurer feat</label>
							</div>
						</li>
						<li className="nav-item text-left pl-1 border-bottom">
							<div className="form-check">
								<input className="form-check-input" type="checkbox" name="addNecromancy"
									checked={this.state.addNecromancy} onChange={this.handleInputChange} disabled />
								<label className="form-check-label">Stench of Necromancy</label>
							</div>
							<div className="form-check">
								<input className="form-check-input" type="checkbox" name="addWizardry"
									checked={this.state.addWizardry} onChange={this.handleInputChange} disabled />
								<label className="form-check-label">Touch of Wizardry</label>
							</div>
							<div className="form-check">
								<input className="form-check-input" type="checkbox" name="addDivine"
									checked={this.state.addDivine} onChange={this.handleInputChange} />
								<label className="form-check-label">Trace of the Divine</label>
							</div>
							<div className="form-check">
								<input className="form-check-input" type="checkbox" name="addSorcery"
									checked={this.state.addSorcery} onChange={this.handleInputChange} disabled />
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
									<button className="btn btn-success" onClick={this.handleDaily}>Next Daily Spell(s)</button>
								</div>
							</div>
						</li>
					</ul></div>
				</div>

				<div className="row text-light">
					<div className="col-lg-6 col-md-12 py-1 bg-secondary border-right">
						<h5>Warp:</h5>
						{warp}
					</div>
					<div className="col-lg-6 col-md-12 py-1 bg-info">
						<h5>High Weirdness:</h5>
						<p>{this.state.currentWeird}</p>
						<p className="bg_feat text_small"><strong>Adventurer Feat:</strong> {weirdnessJSON.feats.adventurer}</p>
						<p className="bg_feat text_small"><strong>Champion Feat:</strong> {weirdnessJSON.feats.champion}</p>
						<p className="bg_feat text_small"><strong>Epic Feat:</strong> {weirdnessJSON.feats.epic}</p>
					</div>
				</div>

				{spells}

			</div>
		);
	}
}
