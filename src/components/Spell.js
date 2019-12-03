import React from 'react';
import './Spell.css';

export default class Spell extends React.Component {
	constructor(props) {
		super(props);
		this.state = props.data;
	}

	render() {
		if (this.props.category === 'attack') var color = 'danger';
		else if (this.props.category === 'defense') color = 'success';
		else color = 'primary';

		if (this.state.target !== undefined) var target = <p><strong>Target(s):</strong> {this.state.target}</p>;

		if (this.state.effect !== undefined) var effect = <p><strong>Effect:</strong> {this.state.effect}</p>;

		if (this.state.attack !== undefined) var attack = <p><strong>Attack:</strong> {this.state.attack}</p>;

		if (this.state.hit !== undefined) var hit = <p><strong>Hit:</strong> {this.state.hit}</p>;

		if (this.state.miss !== undefined) var miss = <p><strong>Miss:</strong> {this.state.miss}</p>;

		if (this.state.advancement !== undefined) var advancement = <p>{this.state.advancement}</p>;

		if (this.state.feats !== undefined) var feats = (<div>
			<p className="bg_feat"><strong>Adventurer Feat:</strong> {this.state.feats.adventurer}</p>
			<p className="bg_feat"><strong>Champion Feat:</strong> {this.state.feats.champion}</p>
			<p className="bg_feat"><strong>Epic Feat:</strong> {this.state.feats.epic}</p>
		</div>);

		return (
			<div className={`col-lg-6 col-md-12 my-1 rounded border border-${color}`}>
				<h3 className={`text-${color}`}>{this.state.title} {this.state.level}</h3>
				<p>{this.state.type} ◆ <strong>{this.state.frequency}</strong></p>
				{target}
				{effect}
				{attack}
				{hit}
				{miss}
				{advancement}
				{feats}
			</div>
		);
	}
}
