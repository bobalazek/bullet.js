import os

def get_bullet_includes(BULLET_DIRECTORY):
    return [
        ##### General
        os.path.join(BULLET_DIRECTORY, 'src', 'btBulletCollisionCommon.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'btBulletDynamicsCommon.h'),

        ##### Linear Math
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btVector3.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btQuadWord.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btQuaternion.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btMatrix3x3.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btTransform.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btMotionState.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath',
                     'btPoolAllocator.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath',
                     'btDefaultMotionState.h'),

        ##### Bullet Collision

        ### Broadphase Collision
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'BroadphaseCollision', 'btBroadphaseProxy.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'BroadphaseCollision', 'btOverlappingPairCache.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'BroadphaseCollision', 'btDbvt.h'),

        ### Narrow Phase Collision
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'NarrowPhaseCollision', 'btManifoldPoint.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'NarrowPhaseCollision', 'btPersistentManifold.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'NarrowPhaseCollision', 'btVoronoiSimplexSolver.h'),

        ### Collision Dispatch
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionDispatch', 'btCollisionObject.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionDispatch', 'btCollisionObjectWrapper.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionDispatch', 'btCollisionWorld.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionDispatch', 'btCollisionCreateFunc.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionDispatch', 'btCollisionConfiguration.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionDispatch', 'btDefaultCollisionConfiguration.h'),

        ### Collision Shapes
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCollisionShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btBoxShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btSphereShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCapsuleShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCylinderShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btConeShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btStaticPlaneShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btConvexHullShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTriangleMesh.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btConvexTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btBvhTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btScaledBvhTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTriangleIndexVertexArray.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCompoundShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTetrahedronShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btEmptyShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btMultiSphereShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btUniformScalingShape.h'),
    ]

def get_idl_file_paths(ROOT):
    return [
        os.path.join(ROOT, 'data', 'idls', 'LinearMath.idl'),
        os.path.join(ROOT, 'data', 'idls', 'BulletCollision',
                     'CollisionDispatch.idl'),
        os.path.join(ROOT, 'data', 'idls', 'BulletCollision',
                     'CollisionShapes.idl'),
        os.path.join(ROOT, 'data', 'idls', 'BulletCollision',
                     'BroadphaseCollision.idl'),
        os.path.join(ROOT, 'data', 'idls', 'BulletCollision',
                     'NarrowPhaseCollision.idl'),
    ]
