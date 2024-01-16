const width = window.innerWidth, height = window.innerHeight;

// init

const camera = new THREE.PerspectiveCamera( 50, width / height, 0.01, 100 );
camera.position.z = 10;

const scene = new THREE.Scene();
let mesh = new THREE.Mesh();

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setSize( width, height );
document.getElementById("render-region").appendChild( renderer.domElement );

function add_data( vertices, face_indices ) {
	const geometry = new THREE.BufferGeometry();
	geometry.computeVertexNormals()
	geometry.setAttribute(  'position', new THREE.BufferAttribute( vertices, 3 )  );
	geometry.setIndex( face_indices );

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