const width = window.innerWidth, height = window.innerHeight;

// init

const camera = new THREE.PerspectiveCamera( 70, width / height, 0.01, 10 );
camera.position.z = 1;

const scene = new THREE.Scene();
let mesh = new THREE.Mesh();

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setSize( width, height );
document.getElementById("render-region").appendChild( renderer.domElement );

function add_data( data ) {
	const geometry = new THREE.BoxGeometry( 0.2, 0.2, 0.2 );
	const material = new THREE.MeshNormalMaterial();

	mesh = new THREE.Mesh( geometry, material );
	scene.add( mesh );
	renderer.setAnimationLoop( animation );
}


// animation

function animation( time ) {

	mesh.rotation.x = time / 2000;
	mesh.rotation.y = time / 1000;

	renderer.render( scene, camera );

}